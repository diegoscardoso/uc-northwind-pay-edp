"""Deterministic Type 05 Parquet schema and table construction.

`rate_percent` is `decimal128(9, 3)` and every money column is `(18, 2)`. Giving
the rate the money scale would round it before it was ever applied, which is the
one thing this type exists to get right.
"""

from __future__ import annotations

from typing import Sequence

import pyarrow as pa  # type: ignore[import-untyped]  # pyarrow ships no py.typed marker

from ...common.parquet import canonical_metadata
from .model import SanitizedRecord

WRITER_VERSION = "1.0.0"

SCHEMA_FIELDS: tuple[tuple[str, pa.DataType], ...] = (
    ("batch_id", pa.string()),
    ("source_file", pa.string()),
    ("source_record_number", pa.int32()),
    ("assessment_id", pa.string()),
    ("merchant_id", pa.string()),
    ("merchant_tax_id_masked", pa.string()),
    ("fee_code", pa.string()),
    ("description", pa.string()),
    ("gross_amount_brl", pa.decimal128(18, 2)),
    ("rate_percent", pa.decimal128(9, 3)),
    ("assessed_fee_brl", pa.decimal128(18, 2)),
    ("calculated_fee_brl", pa.decimal128(18, 2)),
    ("assessment_date", pa.string()),
    ("rounding_mode", pa.string()),
)


def schema(
    *,
    batch_id: str,
    raw_sha256: str,
    contract_version: int = 1,
    layout_version: str = "001",
) -> pa.Schema:
    return pa.schema(
        [pa.field(name, kind, nullable=False) for name, kind in SCHEMA_FIELDS],
        metadata=canonical_metadata(
            batch_id=batch_id,
            type_number="05",
            contract_code="MER_FEESET05",
            contract_version=contract_version,
            layout_version=layout_version,
            raw_sha256=raw_sha256,
            writer_version=WRITER_VERSION,
        ),
    )


def table(
    records: Sequence[SanitizedRecord],
    *,
    batch_id: str,
    raw_sha256: str,
) -> pa.Table:
    ordered = sorted(records, key=lambda record: record.source_record_number)
    columns = {
        name: [getattr(record, name) for record in ordered]
        for name, _ in SCHEMA_FIELDS
    }
    return pa.Table.from_pydict(
        columns, schema=schema(batch_id=batch_id, raw_sha256=raw_sha256)
    )
