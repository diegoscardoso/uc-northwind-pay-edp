"""Typed Type 05 domain records with exact Decimal money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Assessment:
    """One merchant fee assessment row, still carrying the restricted CNPJ.

    ``calculated_fee`` is this implementation's own HALF_UP computation. It is
    stored beside the source's ``assessed_fee`` rather than replacing it: the
    two being equal is a validated contract rule, not an assumption.
    """

    physical_record_number: int
    assessment_id: str
    batch_id: str
    merchant_id: str
    merchant_tax_id: str
    fee_code: str
    description: str
    gross_amount: Decimal
    rate_percent: Decimal
    assessed_fee: Decimal
    calculated_fee: Decimal
    assessment_date: date


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    batch_id: str
    file_date: date
    rows: tuple[Assessment, ...]
    computed_row_count: int
    computed_gross_amount: Decimal
    computed_assessed_fee: Decimal
    computed_calculated_fee: Decimal


@dataclass(frozen=True, slots=True)
class SanitizedRecord:
    batch_id: str
    source_file: str
    source_record_number: int
    assessment_id: str
    merchant_id: str
    merchant_tax_id_masked: str
    fee_code: str
    description: str
    gross_amount_brl: Decimal
    rate_percent: Decimal
    assessed_fee_brl: Decimal
    calculated_fee_brl: Decimal
    assessment_date: str
    rounding_mode: str
