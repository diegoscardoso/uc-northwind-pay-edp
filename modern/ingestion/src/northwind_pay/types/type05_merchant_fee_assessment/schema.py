"""Validate a parsed Type 05 batch and produce its sanitized records.

This is where the source's declaration is confronted with what its own rows add
up to. When they disagree the batch is refused and **the declaration is carried
forward untouched** — repairing it would destroy the evidence that something
upstream is broken.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal

from ...common.money import render
from ...common.privacy import assert_no_restricted_values, mask_document
from .model import ParsedBatch, SanitizedBatch, SanitizedRecord
from .parser import calculated_fee

ASSESSMENT_ID = re.compile(r"^FEE[0-9]{13}$")
MERCHANT_ID = re.compile(r"^MER[0-9]{13}$")
FEE_CODE = re.compile(r"^[A-Z][A-Z0-9_]{1,9}$")
BATCH_ID = re.compile(r"^B[0-9]{15}$")
MAX_DESCRIPTION_CODEPOINTS = 80
ROUNDING_MODE = "HALF_UP"


class SchemaError(ValueError):
    """The batch does not satisfy the Type 05 contract."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class Controls:
    """Both sides of every control, so a difference stays visible."""

    declared_row_count: int
    computed_row_count: int
    declared_gross_amount: Decimal
    computed_gross_amount: Decimal
    declared_assessed_fee: Decimal
    computed_assessed_fee: Decimal
    declared_calculated_fee: Decimal
    computed_calculated_fee: Decimal
    currency: str

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_assessed_fee": render(self.computed_assessed_fee),
            "computed_calculated_fee": render(self.computed_calculated_fee),
            "computed_gross_amount": render(self.computed_gross_amount),
            "computed_row_count": self.computed_row_count,
            "currency": self.currency,
            "declared_assessed_fee": render(self.declared_assessed_fee),
            "declared_calculated_fee": render(self.declared_calculated_fee),
            "declared_gross_amount": render(self.declared_gross_amount),
            "declared_row_count": self.declared_row_count,
        }


def controls_of(parsed: ParsedBatch) -> Controls:
    return Controls(
        declared_row_count=parsed.declared.row_count,
        computed_row_count=parsed.computed_row_count,
        declared_gross_amount=parsed.declared.gross_amount,
        computed_gross_amount=parsed.computed_gross_amount,
        declared_assessed_fee=parsed.declared.assessed_fee,
        computed_assessed_fee=parsed.computed_assessed_fee,
        declared_calculated_fee=parsed.declared.calculated_fee,
        computed_calculated_fee=parsed.computed_calculated_fee,
        currency=parsed.declared.currency,
    )


def sanitize(parsed: ParsedBatch, *, source_filename: str) -> SanitizedBatch:
    if not parsed.assessments:
        raise SchemaError("EMPTY_BATCH", "batch carries no assessments")

    batch_id = parsed.assessments[0].batch_id
    if not BATCH_ID.fullmatch(batch_id):
        raise SchemaError("INVALID_BATCH_ID", "batch identity is malformed")

    seen: set[str] = set()
    records: list[SanitizedRecord] = []
    for item in parsed.assessments:
        where = f"record {item.physical_record_number}"
        if item.batch_id != batch_id:
            raise SchemaError("CROSS_BATCH_ROW", f"{where}: batch identity differs")
        if not ASSESSMENT_ID.fullmatch(item.assessment_id):
            raise SchemaError("INVALID_ASSESSMENT_ID", where)
        if item.assessment_id in seen:
            raise SchemaError("DUPLICATE_ASSESSMENT_ID", where)
        seen.add(item.assessment_id)
        if not MERCHANT_ID.fullmatch(item.merchant_id):
            raise SchemaError("INVALID_MERCHANT_ID", where)
        if not FEE_CODE.fullmatch(item.fee_code):
            raise SchemaError("INVALID_FEE_CODE", where)
        normalized = unicodedata.normalize("NFC", item.description)
        if not 1 <= len(normalized) <= MAX_DESCRIPTION_CODEPOINTS:
            raise SchemaError("INVALID_DESCRIPTION", where)
        if item.gross_amount_brl <= Decimal("0.00"):
            raise SchemaError("INVALID_GROSS_AMOUNT", where)
        if not Decimal("0.000") < item.rate_percent <= Decimal("100.000"):
            raise SchemaError("INVALID_RATE_PERCENT", where)

        # The row's own arithmetic must hold before the batch total is judged.
        expected = calculated_fee(item)
        if item.assessed_fee_brl != expected:
            raise SchemaError(
                "ROW_FEE_CALCULATION_MISMATCH",
                f"{where}: assessed {item.assessed_fee_brl} but HALF_UP gives {expected}",
            )

        records.append(
            SanitizedRecord(
                batch_id=batch_id,
                source_file=source_filename,
                source_record_number=item.physical_record_number,
                assessment_id=item.assessment_id,
                merchant_id=item.merchant_id,
                merchant_tax_id_masked=mask_document(item.merchant_tax_id),
                fee_code=item.fee_code,
                description=normalized,
                gross_amount_brl=item.gross_amount_brl,
                rate_percent=item.rate_percent,
                assessed_fee_brl=item.assessed_fee_brl,
                calculated_fee_brl=expected,
                assessment_date=item.assessment_date.isoformat(),
                rounding_mode=ROUNDING_MODE,
            )
        )

    controls = controls_of(parsed)
    _refuse_on_source_disagreement(controls)

    # Layer three: the finished output is scanned for every raw tax identifier.
    payload = "\n".join(
        ",".join(
            [
                record.batch_id,
                record.source_file,
                str(record.source_record_number),
                record.assessment_id,
                record.merchant_id,
                record.merchant_tax_id_masked,
                record.fee_code,
                record.description,
                render(record.gross_amount_brl),
                f"{record.rate_percent:.3f}",
                render(record.assessed_fee_brl),
                render(record.calculated_fee_brl),
                record.assessment_date,
                record.rounding_mode,
            ]
        )
        for record in records
    )
    assert_no_restricted_values(
        payload, tuple(item.merchant_tax_id for item in parsed.assessments)
    )

    return SanitizedBatch(batch_id=batch_id, records=tuple(records))


def _refuse_on_source_disagreement(controls: Controls) -> None:
    """Refuse when the source's declaration contradicts its own rows.

    Each control is compared separately and the first disagreement names itself,
    so the finding says which number was wrong rather than that something was.
    """

    if controls.declared_row_count != controls.computed_row_count:
        raise SchemaError(
            "SOURCE_CONTROL_ROW_COUNT_MISMATCH",
            f"declared {controls.declared_row_count}, computed {controls.computed_row_count}",
        )
    if controls.declared_gross_amount != controls.computed_gross_amount:
        raise SchemaError(
            "SOURCE_CONTROL_GROSS_MISMATCH",
            f"declared {render(controls.declared_gross_amount)}, "
            f"computed {render(controls.computed_gross_amount)}",
        )
    if controls.declared_assessed_fee != controls.computed_assessed_fee:
        raise SchemaError(
            "SOURCE_CONTROL_ASSESSED_FEE_MISMATCH",
            f"declared {render(controls.declared_assessed_fee)}, "
            f"computed {render(controls.computed_assessed_fee)}",
        )
    if controls.declared_calculated_fee != controls.computed_calculated_fee:
        raise SchemaError(
            "SOURCE_CONTROL_CALCULATED_FEE_MISMATCH",
            f"declared {render(controls.declared_calculated_fee)}, "
            f"computed {render(controls.computed_calculated_fee)}",
        )
