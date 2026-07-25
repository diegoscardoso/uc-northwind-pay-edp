"""The dlt boundary: registration, never transformation.

dlt loads already-canonical landing Parquet into DuckDB and owns load identity
and state. It does not parse, does not derive a value, and does not reshape a
column — the writer already decided all of that. See DR-008.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import pyarrow.parquet as pq

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LANDING = REPOSITORY_ROOT / "modern" / "landing"
DEFAULT_DATABASE = (
    REPOSITORY_ROOT / "modern" / "lakehouse" / "ducklake" / "northwind_modern.duckdb"
)

# One landing table per approved type. Names are fixed by the contract, never
# inferred from a file name.
TABLE_BY_TYPE = {
    "01": "card_settlement",
    "02": "instant_payment_event",
    "03": "payment_slip_settlement",
    "04": "ted_transfer_movement",
    "05": "merchant_fee_assessment",
}


@dataclass(frozen=True, slots=True)
class RegistrationResult:
    """What dlt registered, and under which load identity."""

    dataset: str
    table: str
    load_id: str
    row_count: int
    parquet_files: tuple[str, ...]


def landing_files(landing_root: Path, type_number: str) -> list[Path]:
    """Return every published Parquet file for one type, deterministically."""

    suffix = {
        "01": "NW_CARD_SETTLEMENT",
        "02": "NW_INSTANT_PAYMENT",
        "03": "NW_PAYMENT_SLIP",
        "04": "NW_TED_SETTLEMENT",
        "05": "NW_MERCHANT_FEES",
    }[type_number]
    return sorted(
        path
        for path in landing_root.rglob("*.parquet")
        if path.name.startswith(suffix)
    )


def _arrow_batches(files: list[Path]) -> Iterator[object]:
    for path in files:
        yield pq.read_table(path)


def _batch_controls(files: list[Path], type_number: str) -> Iterator[dict[str, object]]:
    """Yield the per-batch control manifest the writer published alongside data.

    Registering the declared controls as their own table is what lets Gold
    compare a source-owned declaration against independently computed totals
    without any model re-deriving the declaration itself.
    """

    for path in files:
        manifest_path = path.parent / "parquet-manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        # A writer may publish more declared/computed control pairs than the
        # canonical four keys below — Type 05's contract declares four separate
        # money controls. They travel as text for the same reason net_amount
        # does, and passing them through here is what lets Gold compare a real
        # source declaration instead of aliasing a staged total.
        extra_controls = {
            key: str(manifest[key])
            for key in sorted(manifest)
            if key.startswith(("declared_", "computed_"))
            and key
            not in {
                "declared_detail_count",
                "computed_detail_count",
                "declared_net_amount",
                "computed_net_amount",
            }
        }
        yield {
            **extra_controls,
            "batch_id": str(manifest["batch_id"]),
            "computed_detail_count": int(manifest["computed_detail_count"]),
            # Monetary controls travel as the contract's own canonical text and
            # are typed once, in dbt. Left as Python Decimals, dlt infers
            # DECIMAL(38,9), and a control compared at a scale the contract
            # never specified is not the comparison the contract asks for.
            "computed_net_amount": str(manifest["computed_net_amount"]),
            "contract_code": str(manifest["contract_code"]),
            "currency": str(manifest.get("currency", "BRL")),
            "declared_detail_count": int(manifest["declared_detail_count"]),
            "declared_net_amount": str(manifest["declared_net_amount"]),
            "parquet_sha256": str(manifest["parquet_sha256"]),
            "raw_sha256": str(manifest["raw_sha256"]),
            "record_count": int(manifest["record_count"]),
            "source_file": str(manifest["source_file"]),
            "type_number": type_number,
        }


def register(
    type_number: str,
    *,
    landing_root: Path = DEFAULT_LANDING,
    database: Path = DEFAULT_DATABASE,
    dataset: str = "landing",
) -> RegistrationResult:
    """Load every landing Parquet file for one type into DuckDB through dlt."""

    import dlt

    files = landing_files(landing_root, type_number)
    table = TABLE_BY_TYPE[type_number]
    if not files:
        return RegistrationResult(
            dataset=dataset, table=table, load_id="", row_count=0, parquet_files=()
        )

    database.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    # dlt writes its own working state; keep it inside the disposable runtime.
    os.environ.setdefault(
        "DLT_DATA_DIR", str(REPOSITORY_ROOT / ".runtime" / "dlt")
    )
    pipeline = dlt.pipeline(
        pipeline_name=f"northwind_modern_type{type_number}",
        destination=dlt.destinations.duckdb(str(database)),
        dataset_name=dataset,
        progress=None,
    )
    info = pipeline.run(
        _arrow_batches(files),
        table_name=table,
        write_disposition="replace",
    )
    pipeline.run(
        _batch_controls(files, type_number),
        table_name=f"{table}_control",
        write_disposition="replace",
    )
    load_ids = getattr(info, "loads_ids", None) or [""]
    row_count = sum(pq.read_metadata(path).num_rows for path in files)
    return RegistrationResult(
        dataset=dataset,
        table=table,
        load_id=str(load_ids[-1]),
        row_count=row_count,
        parquet_files=tuple(str(path.name) for path in files),
    )
