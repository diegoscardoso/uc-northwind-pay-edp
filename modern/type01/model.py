"""Typed shapes for a sanitized Type 01 batch, handed from Judge to Landing.

See docs/seams.md (Swimlane 3 Judge -> Swimlane 4 Landing) and
docs/adrs/0002-type-01-five-file-package-is-the-unit.md.
"""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class SanitizedDetail:
    pan_token: str
    cpf_masked: str
    amount: Decimal


@dataclass
class SanitizedBatch:
    batch_id: str
    net_amount: Decimal
    verdict: str  # "accepted" | "refused" | "quarantined"
    details: list[SanitizedDetail] = field(default_factory=list)
