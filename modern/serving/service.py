"""Read-only service layer over an approved Gold snapshot.

Both the HTTP API and the MCP tools call these functions, so the serving rules
hold on every route rather than on whichever one remembered to check.

Two rules are enforced here, not in the callers:

- only approved Gold is readable; there is no path to landing, Bronze, Silver,
  or any restricted zone, and no arbitrary SQL;
- a batch whose golden-match is unresolved cannot be served at all. A broken
  comparison degrades availability rather than correctness.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DUCKDB_PATH = (
    REPOSITORY_ROOT / "modern" / "lakehouse" / "ducklake" / "northwind_modern.duckdb"
)
EVIDENCE_ROOT = REPOSITORY_ROOT / "evidence" / "modern"

# The complete set of relations this service may read. Anything absent from
# this map is unreachable by construction, not by convention.
GOLD_RELATIONS: Mapping[str, str] = {
    "01": "main_gold.gold_card_settlement_reconciliation",
    "02": "main_gold.gold_instant_payment_reconciliation",
    "03": "main_gold.gold_payment_slip_reconciliation",
    "04": "main_gold.gold_ted_transfer_reconciliation",
    "05": "main_gold.gold_merchant_fee_reconciliation",
}

BATCH_ID_LENGTH = 16


class ServiceError(Exception):
    """A read-only service request cannot be satisfied."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status


@dataclass(frozen=True, slots=True)
class BatchStatus:
    batch_id: str
    status: str
    code: str | None
    golden_match_resolved: bool


def _validate_batch_id(batch_id: str) -> str:
    if (
        len(batch_id) != BATCH_ID_LENGTH
        or not batch_id.startswith("B")
        or not batch_id[1:].isdigit()
    ):
        raise ServiceError(400, "batch identity is malformed")
    return batch_id


def _evidence(batch_id: str, name: str) -> dict[str, Any]:
    path = EVIDENCE_ROOT / batch_id / name
    if not path.is_file():
        raise ServiceError(404, "no modern evidence exists for this batch")
    return json.loads(path.read_text(encoding="utf-8"))


def batch_status(batch_id: str) -> dict[str, Any]:
    """Terminal status and whether its golden-match resolved."""

    batch_id = _validate_batch_id(batch_id)
    final = _evidence(batch_id, "final-status.json")
    match = _evidence(batch_id, "golden-match.json")
    return {
        "batch_id": batch_id,
        "code": final.get("code"),
        "golden_match_resolved": bool(match.get("resolved")),
        "status": final.get("status"),
    }


def golden_match(batch_id: str) -> dict[str, Any]:
    """The structured difference report and its adjudication."""

    batch_id = _validate_batch_id(batch_id)
    return {
        "adjudication": _evidence(batch_id, "difference-adjudication.json"),
        "batch_id": batch_id,
        "golden_match": _evidence(batch_id, "golden-match.json"),
    }


def reconciliation(batch_id: str) -> dict[str, Any]:
    """The approved Gold reconciliation, refused unless golden-match resolved."""

    batch_id = _validate_batch_id(batch_id)
    match = _evidence(batch_id, "golden-match.json")
    if not match.get("resolved"):
        raise ServiceError(
            409, "golden-match is unresolved; this batch is not approved for serving"
        )
    relation = GOLD_RELATIONS.get(str(match.get("type_number")))
    if relation is None:
        raise ServiceError(404, "no approved Gold relation exists for this type")

    import duckdb

    if not DUCKDB_PATH.is_file():
        raise ServiceError(503, "the approved Gold snapshot is not available")
    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    try:
        cursor = connection.execute(
            f"select * from {relation} where batch_id = ?", [batch_id]
        )
        row = cursor.fetchone()
        if row is None:
            raise ServiceError(404, "no approved Gold row exists for this batch")
        columns = [description[0] for description in cursor.description]
        return {
            name: (str(value) if hasattr(value, "as_tuple") else value)
            for name, value in zip(columns, row)
        }
    finally:
        connection.close()


def health() -> dict[str, Any]:
    return {
        "gold_snapshot_available": DUCKDB_PATH.is_file(),
        "served_zone": "gold",
        "status": "healthy",
    }
