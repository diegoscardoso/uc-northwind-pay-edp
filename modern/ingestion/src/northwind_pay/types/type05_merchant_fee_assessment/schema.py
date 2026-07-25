"""Type 05 validation, CNPJ privacy, and independent batch controls.

Type 05 is the type whose declared controls travel in the source manifest
rather than in a trailer record, so the declaration enters here from
admission, is compared against independently computed sums, and is preserved
byte-for-byte in the evidence — especially when it is wrong. Repairing a
declared control would destroy the evidence that the source system lied.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from ...common.privacy import assert_no_restricted_values, mask_document
from .model import ParsedBatch, SanitizedRecord

SOURCE_CONTROL_COUNT_MISMATCH = "SOURCE_CONTROL_COUNT_MISMATCH"
SOURCE_CONTROL_GROSS_MISMATCH = "SOURCE_CONTROL_GROSS_MISMATCH"
SOURCE_CONTROL_ASSESSED_FEE_MISMATCH = "SOURCE_CONTROL_ASSESSED_FEE_MISMATCH"
SOURCE_CONTROL_CALCULATED_FEE_MISMATCH = "SOURCE_CONTROL_CALCULATED_FEE_MISMATCH"

ROUNDING_MODE = "HALF_UP"


class SchemaError(ValueError):
    """The parsed batch cannot become a valid sanitized publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class BatchControls:
    declared_row_count: int
    computed_row_count: int
    declared_gross_amount: Decimal
    computed_gross_amount: Decimal
    declared_assessed_fee: Decimal
    computed_assessed_fee: Decimal
    declared_calculated_fee: Decimal
    computed_calculated_fee: Decimal

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_assessed_fee": f"{self.computed_assessed_fee:.2f}",
            "computed_calculated_fee": f"{self.computed_calculated_fee:.2f}",
            "computed_gross_amount": f"{self.computed_gross_amount:.2f}",
            "computed_row_count": self.computed_row_count,
            "declared_assessed_fee": f"{self.declared_assessed_fee:.2f}",
            "declared_calculated_fee": f"{self.declared_calculated_fee:.2f}",
            "declared_gross_amount": f"{self.declared_gross_amount:.2f}",
            "declared_row_count": self.declared_row_count,
        }


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    batch_id: str
    source_file: str
    records: tuple[SanitizedRecord, ...]
    controls: BatchControls


def _declared_count(declared: Mapping[str, Any]) -> int:
    value = declared.get("row_count")
    if isinstance(value, bool) or not isinstance(value, int):
        raise SchemaError(
            SOURCE_CONTROL_COUNT_MISMATCH,
            "the declared row count is absent or not an integer",
        )
    return value


def _declared_money(declared: Mapping[str, Any], name: str, code: str) -> Decimal:
    value = declared.get(name)
    try:
        amount = Decimal(str(value))
    except InvalidOperation as exc:
        raise SchemaError(code, "a declared control is absent or not money") from exc
    return amount


def controls_of(
    parsed: ParsedBatch, declared: Mapping[str, Any]
) -> BatchControls:
    """Pair the source manifest's declaration with independent computation.

    The declared values are carried exactly as published — no quantize, no
    repair — so a wrong declaration survives into evidence as itself.
    """

    return BatchControls(
        declared_row_count=_declared_count(declared),
        computed_row_count=parsed.computed_row_count,
        declared_gross_amount=_declared_money(
            declared, "gross_amount", SOURCE_CONTROL_GROSS_MISMATCH
        ),
        computed_gross_amount=parsed.computed_gross_amount,
        declared_assessed_fee=_declared_money(
            declared, "assessed_fee", SOURCE_CONTROL_ASSESSED_FEE_MISMATCH
        ),
        computed_assessed_fee=parsed.computed_assessed_fee,
        declared_calculated_fee=_declared_money(
            declared, "calculated_fee", SOURCE_CONTROL_CALCULATED_FEE_MISMATCH
        ),
        computed_calculated_fee=parsed.computed_calculated_fee,
    )


def sanitize(
    parsed: ParsedBatch,
    *,
    source_filename: str,
    declared: Mapping[str, Any],
) -> SanitizedBatch:
    """Validate the four source controls, mask the CNPJ, and emit source order."""

    controls = controls_of(parsed, declared)
    for declared_value, computed_value, code in (
        (
            controls.declared_row_count,
            controls.computed_row_count,
            SOURCE_CONTROL_COUNT_MISMATCH,
        ),
        (
            controls.declared_gross_amount,
            controls.computed_gross_amount,
            SOURCE_CONTROL_GROSS_MISMATCH,
        ),
        (
            controls.declared_assessed_fee,
            controls.computed_assessed_fee,
            SOURCE_CONTROL_ASSESSED_FEE_MISMATCH,
        ),
        (
            controls.declared_calculated_fee,
            controls.computed_calculated_fee,
            SOURCE_CONTROL_CALCULATED_FEE_MISMATCH,
        ),
    ):
        if declared_value != computed_value:
            raise SchemaError(code, "a declared source control is wrong")

    records = tuple(
        SanitizedRecord(
            batch_id=parsed.batch_id,
            source_file=source_filename,
            source_record_number=row.physical_record_number,
            assessment_id=row.assessment_id,
            merchant_id=row.merchant_id,
            merchant_tax_id_masked=mask_document(row.merchant_tax_id),
            fee_code=row.fee_code,
            description=row.description,
            gross_amount_brl=row.gross_amount,
            rate_percent=row.rate_percent,
            assessed_fee_brl=row.assessed_fee,
            calculated_fee_brl=row.calculated_fee,
            assessment_date=row.assessment_date.isoformat(),
            rounding_mode=ROUNDING_MODE,
        )
        for row in parsed.rows
    )

    restricted = tuple(row.merchant_tax_id for row in parsed.rows)
    candidate = "\n".join(
        ",".join(
            (
                record.batch_id,
                record.source_file,
                str(record.source_record_number),
                record.assessment_id,
                record.merchant_id,
                record.merchant_tax_id_masked,
                record.fee_code,
                record.description,
                f"{record.gross_amount_brl:.2f}",
                f"{record.rate_percent:.3f}",
                f"{record.assessed_fee_brl:.2f}",
                f"{record.calculated_fee_brl:.2f}",
                record.assessment_date,
                record.rounding_mode,
            )
        )
        for record in records
    )
    assert_no_restricted_values(candidate, restricted)

    return SanitizedBatch(
        batch_id=parsed.batch_id,
        source_file=source_filename,
        records=records,
        controls=controls,
    )
