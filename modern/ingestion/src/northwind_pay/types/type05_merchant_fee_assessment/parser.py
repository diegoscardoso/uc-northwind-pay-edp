"""Independent Type 05 transport and grammar parser.

Implements ``contracts/types/05-merchant-fee-assessment/layout.yaml``: strict
NFC UTF-8 without BOM, LF-only transport with a required final LF, a
semicolon-delimited grammar read by a single-pass quote-aware lexer in which
only the description may — and must — be quoted, decimal commas at fixed
scales, dd/MM/yyyy dates, Mod-11 CNPJ validation, and the per-row HALF_UP fee
recomputation.

Rejection codes come from the contract's ``canonical_rejection_codes``. Two
groupings the contract names but does not code individually are mapped here:
the ``max_detail_rows`` bound refuses as ``INVALID_SOURCE_SIZE`` (it is a
file-size bound counted in rows), and a row whose batch identity contradicts
the filename refuses as ``INVALID_BUSINESS_DATE`` (the contract folds batch
and date into one ``filename_batch_and_business_date_rules`` group).
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from ...common.documents import DocumentError, validate_cnpj
from .model import Assessment, ParsedBatch

FILENAME = re.compile(r"^NW_MERCHANT_FEES_([0-9]{8})_(B[0-9]{15})\.csv$")
ASSESSMENT_ID = re.compile(r"^FEE[0-9]{13}$")
BATCH_ID = re.compile(r"^B[0-9]{15}$")
MERCHANT_ID = re.compile(r"^MER[0-9]{13}$")
FEE_CODE = re.compile(r"^[A-Z][A-Z0-9_]{1,9}$")
GROSS_AMOUNT = re.compile(r"^(0|[1-9][0-9]{0,11}),[0-9]{2}$")
RATE_PERCENT = re.compile(r"^(0|[1-9][0-9]{0,2}),[0-9]{3}$")
ASSESSED_FEE = re.compile(r"^(0|[1-9][0-9]{0,11}),[0-9]{2}$")
ASSESSMENT_DATE = re.compile(r"^([0-9]{2})/([0-9]{2})/([0-9]{4})$")
FORBIDDEN_DIGIT_RUN = re.compile(r"[0-9]{11}")

HEADER = (
    "assessment_id;batch_id;merchant_id;merchant_tax_id;fee_code;description;"
    "gross_amount_brl;rate_percent;assessed_fee_brl;assessment_date"
)

FIELD_COUNT = 10
DESCRIPTION_INDEX = 5
MAX_SOURCE_FILE_BYTES = 5130138
MAX_PHYSICAL_RECORD_BYTES = 512
MAX_DETAIL_ROWS = 10000
MAX_DESCRIPTION_CODEPOINTS = 80
RATE_MAXIMUM = Decimal("100.000")
CENT = Decimal("0.01")

FILE_TYPE_CODE = "MER_FEESET05"
LAYOUT_VERSION = "001"

# The contract forbids C0 controls, C1 controls, and the bidirectional control
# characters inside a description. Unicode categories Cc and Cf cover exactly
# those (Cf includes every bidi control), and nothing the contract allows.
_FORBIDDEN_CATEGORIES = {"Cc", "Cf"}
_FORBIDDEN_PREFIXES = ("=", "+", "-", "@")


class ParseError(ValueError):
    """The raw batch violates its transport or grammar contract.

    Codes come from ``canonical_rejection_codes`` in the type's own layout
    contract.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _lex(record: str) -> list[tuple[str, bool]]:
    """Split one record into ``(value, was_quoted)`` fields in a single pass.

    The lexer enforces the grammar's quoting rules as it reads: doubled quotes
    escape inside a quoted field, a quote may open only at a field boundary,
    nothing may follow a closing quote but a delimiter, and no whitespace
    exists outside quotes because no field may contain one unquoted.
    """

    fields: list[tuple[str, bool]] = []
    value: list[str] = []
    quoted = False
    in_quotes = False
    position = 0
    length = len(record)

    while position < length:
        character = record[position]
        if in_quotes:
            if character == '"':
                if position + 1 < length and record[position + 1] == '"':
                    value.append('"')
                    position += 2
                    continue
                in_quotes = False
                position += 1
                if position < length and record[position] != ";":
                    raise ParseError(
                        "INVALID_CSV_QUOTING",
                        "content follows a closing quote before the delimiter",
                    )
                continue
            value.append(character)
            position += 1
            continue
        if character == '"':
            if value or quoted:
                raise ParseError(
                    "INVALID_CSV_QUOTING", "a quote opens inside a field"
                )
            in_quotes = True
            quoted = True
            position += 1
            continue
        if character == ";":
            fields.append(("".join(value), quoted))
            value = []
            quoted = False
            position += 1
            continue
        if not quoted:
            value.append(character)
            position += 1
            continue
        raise ParseError(
            "INVALID_CSV_QUOTING", "content follows a closing quote"
        )

    if in_quotes:
        raise ParseError("INVALID_CSV_QUOTING", "a quoted field never closes")
    fields.append(("".join(value), quoted))
    return fields


def _decimal_comma(text: str, pattern: re.Pattern[str], code: str) -> Decimal:
    if not pattern.match(text):
        raise ParseError(code, "a decimal field is not in canonical comma form")
    return Decimal(text.replace(",", "."))


def _description(text: str, merchant_tax_id: str) -> str:
    if not 1 <= len(text) <= MAX_DESCRIPTION_CODEPOINTS:
        raise ParseError(
            "INVALID_DESCRIPTION", "a description length is out of bounds"
        )
    if unicodedata.normalize("NFC", text) != text:
        raise ParseError(
            "INVALID_DESCRIPTION", "a description is not NFC-normalized"
        )
    if any(unicodedata.category(char) in _FORBIDDEN_CATEGORIES for char in text):
        raise ParseError(
            "INVALID_DESCRIPTION", "a description carries a control character"
        )
    if text.startswith(_FORBIDDEN_PREFIXES):
        raise ParseError(
            "INVALID_DESCRIPTION", "a description starts like a formula"
        )
    if FORBIDDEN_DIGIT_RUN.search(text):
        raise ParseError(
            "INVALID_DESCRIPTION", "a description carries a long digit run"
        )
    if merchant_tax_id in text:
        raise ParseError(
            "INVALID_DESCRIPTION", "a description carries a raw tax identifier"
        )
    return text


def _date(text: str) -> date:
    match = ASSESSMENT_DATE.match(text)
    if match is None:
        raise ParseError("INVALID_FIELD", "a date field is not dd/MM/yyyy")
    day, month, year = (int(part) for part in match.groups())
    try:
        return date(year, month, day)
    except ValueError as exc:
        raise ParseError(
            "INVALID_FIELD", "a date field is not a valid calendar date"
        ) from exc


def _parse_row(
    record: str,
    number: int,
    *,
    filename_batch: str,
    file_date: date,
) -> Assessment:
    fields = _lex(record)
    if len(fields) != FIELD_COUNT:
        raise ParseError("INVALID_FIELD_COUNT", "a row does not carry ten fields")
    for index, (value, was_quoted) in enumerate(fields):
        if index == DESCRIPTION_INDEX:
            if not was_quoted:
                raise ParseError(
                    "INVALID_CSV_QUOTING", "the description is not quoted"
                )
        elif was_quoted:
            raise ParseError(
                "INVALID_CSV_QUOTING", "a non-description field is quoted"
            )
        elif any(character.isspace() for character in value):
            raise ParseError(
                "INVALID_CSV_QUOTING", "whitespace appears outside quotes"
            )
        if not value:
            raise ParseError("INVALID_FIELD", "an empty field is forbidden")

    values = [value for value, _ in fields]

    assessment_id = values[0]
    if not ASSESSMENT_ID.match(assessment_id):
        raise ParseError("INVALID_IDENTIFIER", "an assessment identity is malformed")
    row_batch = values[1]
    if not BATCH_ID.match(row_batch):
        raise ParseError("INVALID_IDENTIFIER", "a row batch identity is malformed")
    merchant_id = values[2]
    if not MERCHANT_ID.match(merchant_id):
        raise ParseError("INVALID_IDENTIFIER", "a merchant identity is malformed")
    try:
        merchant_tax_id = validate_cnpj(values[3])
    except DocumentError as exc:
        raise ParseError("INVALID_DOCUMENT", "a merchant document is invalid") from exc
    fee_code = values[4]
    if not FEE_CODE.match(fee_code):
        raise ParseError("INVALID_IDENTIFIER", "a fee code is malformed")
    description = _description(values[5], merchant_tax_id)

    gross_amount = _decimal_comma(values[6], GROSS_AMOUNT, "INVALID_FIELD")
    if gross_amount <= 0:
        raise ParseError("INVALID_FIELD", "a gross amount is not positive")
    rate_percent = _decimal_comma(values[7], RATE_PERCENT, "INVALID_FIELD")
    if rate_percent <= 0 or rate_percent > RATE_MAXIMUM:
        raise ParseError("INVALID_FIELD", "a rate is outside its contract bounds")
    assessed_fee = _decimal_comma(values[8], ASSESSED_FEE, "INVALID_FIELD")

    assessment_date = _date(values[9])
    if row_batch != filename_batch or assessment_date != file_date:
        raise ParseError(
            "INVALID_BUSINESS_DATE",
            "a row does not belong to the filename batch and date",
        )

    # The contract's calculation rule, computed independently: arbitrary
    # precision throughout, one quantize at final scale, HALF_UP. Neither
    # ``round()`` nor ``f"{...:.2f}"`` appears here — both are HALF_EVEN.
    calculated_fee = (gross_amount * rate_percent / 100).quantize(
        CENT, rounding=ROUND_HALF_UP
    )
    if assessed_fee != calculated_fee:
        raise ParseError(
            "FEE_CALCULATION_MISMATCH",
            "an assessed fee is not its independent HALF_UP calculation",
        )

    return Assessment(
        physical_record_number=number,
        assessment_id=assessment_id,
        batch_id=row_batch,
        merchant_id=merchant_id,
        merchant_tax_id=merchant_tax_id,
        fee_code=fee_code,
        description=description,
        gross_amount=gross_amount,
        rate_percent=rate_percent,
        assessed_fee=assessed_fee,
        calculated_fee=calculated_fee,
        assessment_date=assessment_date,
    )


def parse(payload: bytes, *, source_filename: str) -> ParsedBatch:
    """Parse one raw batch and compute its controls independently."""

    filename_match = FILENAME.match(source_filename)
    if filename_match is None:
        raise ParseError("INVALID_TRANSPORT", "the source filename is malformed")
    filename_date_text, filename_batch = filename_match.groups()
    try:
        file_date = date(
            int(filename_date_text[0:4]),
            int(filename_date_text[4:6]),
            int(filename_date_text[6:8]),
        )
    except ValueError as exc:
        raise ParseError(
            "INVALID_TRANSPORT", "the filename date is not a calendar date"
        ) from exc

    if len(payload) > MAX_SOURCE_FILE_BYTES:
        raise ParseError("INVALID_SOURCE_SIZE", "the file exceeds its byte bound")
    if payload.startswith(b"\xef\xbb\xbf"):
        raise ParseError("INVALID_UTF8", "a byte-order mark is forbidden")
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ParseError("INVALID_UTF8", "the file is not strict UTF-8") from exc
    if unicodedata.normalize("NFC", text) != text:
        raise ParseError(
            "INVALID_UNICODE_NORMALIZATION", "the file is not NFC-normalized"
        )
    if "\r" in text:
        raise ParseError("INVALID_TRANSPORT", "a bare CR byte appears")
    if not text.endswith("\n"):
        raise ParseError("INVALID_TRANSPORT", "the file has no final LF")
    records = text.split("\n")[:-1]
    if any(not record for record in records):
        raise ParseError("INVALID_TRANSPORT", "blank lines are forbidden")
    for record in records:
        if len(record.encode("utf-8")) > MAX_PHYSICAL_RECORD_BYTES:
            raise ParseError(
                "INVALID_RECORD_LENGTH", "a record exceeds its byte bound"
            )

    if not records or records[0] != HEADER:
        raise ParseError("INVALID_HEADER", "the header row is not exact")
    if len(records) - 1 > MAX_DETAIL_ROWS:
        raise ParseError("INVALID_SOURCE_SIZE", "the file exceeds its row bound")

    rows: list[Assessment] = []
    identities: set[str] = set()
    for index, record in enumerate(records[1:], start=2):
        row = _parse_row(
            record, index, filename_batch=filename_batch, file_date=file_date
        )
        if row.assessment_id in identities:
            raise ParseError(
                "DUPLICATE_IDENTIFIER", "an assessment identity repeats"
            )
        identities.add(row.assessment_id)
        rows.append(row)

    zero = Decimal("0.00")
    return ParsedBatch(
        batch_id=filename_batch,
        file_date=file_date,
        rows=tuple(rows),
        computed_row_count=len(rows),
        computed_gross_amount=sum((row.gross_amount for row in rows), start=zero),
        computed_assessed_fee=sum((row.assessed_fee for row in rows), start=zero),
        computed_calculated_fee=sum(
            (row.calculated_fee for row in rows), start=zero
        ),
    )
