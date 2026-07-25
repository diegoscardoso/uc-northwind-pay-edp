"""Read Type 05 bytes: semicolon CSV, decimal commas, localized dates.

The grammar is small and the traps are not. A semicolon inside a quoted field is
content, not a delimiter. A doubled quote is one quote. `1,235` is one thousand
two hundred and thirty five thousandths, not one and a fraction — the comma is
the decimal separator, and the thousands separator does not exist in this
layout.

Nothing here rounds. The parser reports what the bytes say; deciding whether the
source told the truth belongs to `schema.py`.
"""

from __future__ import annotations

import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from .model import Assessment, DeclaredControls, ParsedBatch

DELIMITER = ";"
QUOTE = '"'
EXPECTED_HEADER = (
    "assessment_id;batch_id;merchant_id;merchant_tax_id;fee_code;description;"
    "gross_amount_brl;rate_percent;assessed_fee_brl;assessment_date"
)
FIELD_COUNT = 10
DESCRIPTION_POSITION = 5
MAX_ROWS = 10_000


class ParseError(ValueError):
    """The bytes do not satisfy the Type 05 layout contract."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _split_row(line: str, *, record_number: int) -> list[tuple[str, bool]]:
    """Split one semicolon row into (value, was_quoted) pairs.

    Whether a field arrived quoted is part of the contract, not a detail of
    parsing: `description_must_be_quoted` and
    `non_description_fields_must_be_unquoted` are both binding, so the flag has
    to survive the lexer rather than being discarded with the quotes.
    """

    fields: list[tuple[str, bool]] = []
    current: list[str] = []
    quoted = False
    index = 0
    length = len(line)
    while index <= length:
        if index == length:
            fields.append(("".join(current), quoted))
            break
        character = line[index]
        if character == QUOTE:
            if current:
                raise ParseError(
                    "INVALID_CSV_QUOTING",
                    f"record {record_number}: quote opens mid-field",
                )
            quoted = True
            index += 1
            while True:
                if index >= length:
                    raise ParseError(
                        "INVALID_CSV_QUOTING",
                        f"record {record_number}: unterminated quoted field",
                    )
                if line[index] == QUOTE:
                    if index + 1 < length and line[index + 1] == QUOTE:
                        current.append(QUOTE)
                        index += 2
                        continue
                    index += 1
                    break
                current.append(line[index])
                index += 1
            if index < length and line[index] != DELIMITER:
                raise ParseError(
                    "INVALID_CSV_QUOTING",
                    f"record {record_number}: content after closing quote",
                )
            fields.append(("".join(current), True))
            current = []
            quoted = False
            index += 1
            continue
        if character == DELIMITER:
            fields.append(("".join(current), quoted))
            current = []
            quoted = False
            index += 1
            continue
        current.append(character)
        index += 1
    return fields


def _decimal(text: str, *, record_number: int, field: str, scale: int) -> Decimal:
    """Parse a decimal-comma number at an exact scale, refusing anything else."""

    if "." in text or text.count(",") != 1:
        raise ParseError(
            "INVALID_DECIMAL_FORMAT",
            f"record {record_number}: {field} is not decimal-comma",
        )
    whole, _, fraction = text.partition(",")
    if not whole.isdigit() or not fraction.isdigit() or len(fraction) != scale:
        raise ParseError(
            "INVALID_DECIMAL_FORMAT",
            f"record {record_number}: {field} is not scale {scale}",
        )
    try:
        return Decimal(f"{whole}.{fraction}")
    except InvalidOperation as error:  # pragma: no cover - guarded above
        raise ParseError(
            "INVALID_DECIMAL_FORMAT", f"record {record_number}: {field}"
        ) from error


def _date(text: str, *, record_number: int) -> date:
    parts = text.split("/")
    if len(parts) != 3 or [len(part) for part in parts] != [2, 2, 4]:
        raise ParseError(
            "INVALID_DATE_FORMAT", f"record {record_number}: not dd/MM/yyyy"
        )
    try:
        return date(int(parts[2]), int(parts[1]), int(parts[0]))
    except ValueError as error:
        raise ParseError(
            "INVALID_DATE_FORMAT", f"record {record_number}: not a real date"
        ) from error


def _declared(controls: Mapping[str, Any]) -> DeclaredControls:
    """Take the source's own declaration verbatim. Never repair it."""

    try:
        return DeclaredControls(
            row_count=int(controls["row_count"]),
            gross_amount=Decimal(str(controls["gross_amount"])),
            assessed_fee=Decimal(str(controls["assessed_fee"])),
            calculated_fee=Decimal(str(controls["calculated_fee"])),
            currency=str(controls["currency"]),
        )
    except (KeyError, InvalidOperation, ValueError) as error:
        raise ParseError(
            "INVALID_SOURCE_CONTROLS", "source manifest controls are unreadable"
        ) from error


def parse(payload: bytes, *, declared_controls: Mapping[str, Any]) -> ParsedBatch:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ParseError("INVALID_ENCODING", "payload is not UTF-8") from error
    if text.startswith("﻿"):
        raise ParseError("INVALID_ENCODING", "payload carries a byte order mark")
    if "\r" in text:
        raise ParseError("INVALID_LINE_ENDING", "payload carries a carriage return")
    if not text.endswith("\n"):
        raise ParseError("INVALID_LINE_ENDING", "payload has no final newline")

    lines = text[:-1].split("\n")
    if not lines or lines[0] != EXPECTED_HEADER:
        raise ParseError("INVALID_HEADER", "header row does not match the contract")
    if len(lines) - 1 > MAX_ROWS:
        raise ParseError("ROW_COUNT_EXCEEDED", "row count exceeds the contract bound")
    if len(lines) < 2:
        raise ParseError("EMPTY_BATCH", "batch carries no detail rows")

    assessments: list[Assessment] = []
    for offset, line in enumerate(lines[1:]):
        record_number = offset + 2
        cells = _split_row(line, record_number=record_number)
        if len(cells) != FIELD_COUNT:
            raise ParseError(
                "INVALID_FIELD_COUNT",
                f"record {record_number}: {len(cells)} fields, expected {FIELD_COUNT}",
            )
        fields = [value for value, _ in cells]

        # The contract binds quoting per position, not per taste.
        if not cells[DESCRIPTION_POSITION][1]:
            raise ParseError(
                "INVALID_CSV_QUOTING",
                f"record {record_number}: description must be quoted",
            )
        for position, (_, was_quoted) in enumerate(cells):
            if position != DESCRIPTION_POSITION and was_quoted:
                raise ParseError(
                    "INVALID_CSV_QUOTING",
                    f"record {record_number}: field {position + 1} must be unquoted",
                )
        for position, value in enumerate(fields):
            if not value:
                raise ParseError(
                    "EMPTY_FIELD", f"record {record_number}: field {position + 1} empty"
                )
            if position != DESCRIPTION_POSITION and value != value.strip():
                raise ParseError(
                    "INVALID_WHITESPACE",
                    f"record {record_number}: field {position + 1} carries whitespace",
                )

        description = unicodedata.normalize("NFC", fields[DESCRIPTION_POSITION])
        assessments.append(
            Assessment(
                physical_record_number=record_number,
                assessment_id=fields[0],
                batch_id=fields[1],
                merchant_id=fields[2],
                merchant_tax_id=fields[3],
                fee_code=fields[4],
                description=description,
                gross_amount_brl=_decimal(
                    fields[6], record_number=record_number, field="gross", scale=2
                ),
                rate_percent=_decimal(
                    fields[7], record_number=record_number, field="rate", scale=3
                ),
                assessed_fee_brl=_decimal(
                    fields[8], record_number=record_number, field="fee", scale=2
                ),
                assessment_date=_date(fields[9], record_number=record_number),
            )
        )

    declared = _declared(declared_controls)
    return ParsedBatch(
        assessments=tuple(assessments),
        declared=declared,
        computed_row_count=len(assessments),
        computed_gross_amount=sum(
            (item.gross_amount_brl for item in assessments), Decimal("0.00")
        ),
        computed_assessed_fee=sum(
            (item.assessed_fee_brl for item in assessments), Decimal("0.00")
        ),
        computed_calculated_fee=sum(
            (calculated_fee(item) for item in assessments), Decimal("0.00")
        ),
    )


def calculated_fee(assessment: Assessment) -> Decimal:
    """gross × rate%, rounded HALF_UP at the cent, as the contract requires.

    Deliberately not `round()` and not an f-string: both use banker's rounding,
    which turns 0.005 into 0.00 rather than 0.01 and produces a one-cent error
    that every structural test would pass.
    """

    from decimal import ROUND_HALF_UP

    exact = assessment.gross_amount_brl * assessment.rate_percent / Decimal(100)
    return exact.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
