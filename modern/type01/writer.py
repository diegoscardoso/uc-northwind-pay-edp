"""Writes an accepted Type 01 batch to deterministic Parquet under modern/landing/.

Re-checks the privacy boundary (docs/adrs/0004) and the exact-decimal rule
(docs/adrs/0003) at this last hop instead of trusting Parse/Judge blindly,
and enforces the kept-lie rule's zero-rows side (docs/adrs/0005): a refused
or quarantined batch writes nothing, no matter what its declared/computed
amounts were.

This module picks no storage engine, warehouse, or lakehouse beyond "Parquet
in modern/landing/" (docs/adrs/0001) -- that boundary is intentional.
"""

import re
from decimal import Decimal
from pathlib import Path
from typing import Optional

import pyarrow as pa
import pyarrow.parquet as pq

from modern.type01.model import SanitizedBatch

_PAN_TOKEN_RE = re.compile(r"^tok_[0-9a-f]{24}$")
_CPF_MASKED_RE = re.compile(r"^\*{7}\d{4}$")
_MONEY_SCALE = 2
_MONEY_TYPE = pa.decimal128(12, _MONEY_SCALE)


class PrivacyOrDecimalViolation(ValueError):
    """Raised when a record reaching the writer boundary is not sanitized.

    This is a boundary defect, not a source defect -- it means something
    upstream of Landing failed to tokenize a PAN, mask a CPF, or carry an
    exact-decimal amount before handing the batch here.
    """


def _check_decimal(value, label: str) -> None:
    if not isinstance(value, Decimal):
        raise PrivacyOrDecimalViolation(f"{label} is {type(value).__name__}, not Decimal")


def _check_detail(detail) -> None:
    if not _PAN_TOKEN_RE.match(detail.pan_token):
        raise PrivacyOrDecimalViolation(f"pan_token is not a tokenized value: {detail.pan_token!r}")
    if not _CPF_MASKED_RE.match(detail.cpf_masked):
        raise PrivacyOrDecimalViolation(f"cpf_masked is not a masked value: {detail.cpf_masked!r}")
    _check_decimal(detail.amount, "detail.amount")


def write_batch(batch: SanitizedBatch, landing_dir: str) -> Optional[str]:
    """Write one accepted batch to ``<landing_dir>/<batch_id>.parquet``.

    Returns the written path, or ``None`` if the batch produced zero rows
    (refused or quarantined). Raises ``PrivacyOrDecimalViolation`` before
    writing anything if any detail carries a raw PAN, a raw CPF, or a
    non-Decimal money value -- checked regardless of the batch's verdict,
    so a refused/quarantined batch that somehow carried unsanitized details
    is still caught, not silently allowed through because it lands nothing.
    """
    _check_decimal(batch.net_amount, "batch.net_amount")
    for detail in batch.details:
        _check_detail(detail)

    if batch.verdict != "accepted":
        return None

    out_dir = Path(landing_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{batch.batch_id}.parquet"

    n = len(batch.details)
    table = pa.table(
        {
            "batch_id": pa.array([batch.batch_id] * n, type=pa.string()),
            "pan_token": pa.array([d.pan_token for d in batch.details], type=pa.string()),
            "cpf_masked": pa.array([d.cpf_masked for d in batch.details], type=pa.string()),
            "amount": pa.array([d.amount for d in batch.details], type=_MONEY_TYPE),
            "net_amount": pa.array([batch.net_amount] * n, type=_MONEY_TYPE),
        }
    )
    pq.write_table(table, out_path)
    return str(out_path)
