"""Typed Type 05 domain records with exact Decimal money.

Two money scales live here on purpose: amounts and fees are scale two, and
`rate_percent` is scale three. Collapsing them to one scale is how a rate gets
silently rounded before it is ever applied.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

RATE_SCALE = 3


@dataclass(frozen=True, slots=True)
class Assessment:
    """One merchant fee assessment, still carrying the restricted tax id."""

    physical_record_number: int
    assessment_id: str
    batch_id: str
    merchant_id: str
    merchant_tax_id: str
    fee_code: str
    description: str
    gross_amount_brl: Decimal
    rate_percent: Decimal
    assessed_fee_brl: Decimal
    assessment_date: date


@dataclass(frozen=True, slots=True)
class DeclaredControls:
    """What the source system says about this batch. Never repaired."""

    row_count: int
    gross_amount: Decimal
    assessed_fee: Decimal
    calculated_fee: Decimal
    currency: str


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    assessments: tuple[Assessment, ...]
    declared: DeclaredControls
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


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    batch_id: str
    records: tuple[SanitizedRecord, ...]
