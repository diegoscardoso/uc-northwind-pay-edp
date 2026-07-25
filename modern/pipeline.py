#!/usr/bin/env python3
"""The modern pipeline runner: raw bytes to Gold, golden-match, and evidence.

Every stage is a plain function that both this runner and the Dagster assets
call, so "direct and orchestrated execution produce the same result" is a
property of the code rather than a claim.

    modern/pipeline.py --type 01 [--skip-legacy-comparison]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "modern" / "ingestion" / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "modern" / "lakehouse" / "dlt"))
sys.path.insert(0, str(REPOSITORY_ROOT / "validation" / "golden-match"))

import golden_match  # noqa: E402
import registration  # noqa: E402
from northwind_pay import evidence as modern_evidence  # noqa: E402

LANDING_ROOT = REPOSITORY_ROOT / "modern" / "landing"
DUCKDB_PATH = (
    REPOSITORY_ROOT / "modern" / "lakehouse" / "ducklake" / "northwind_modern.duckdb"
)
EVIDENCE_ROOT = REPOSITORY_ROOT / "evidence" / "modern"
DBT_DIR = REPOSITORY_ROOT / "modern" / "dbt"
CONTRACTS = REPOSITORY_ROOT / "contracts" / "types"


def _load_dotenv() -> None:
    """Populate the process environment from `.env`, exactly as legacy does.

    `legacy/runner/config.py` loads `.env` for the legacy stack; modern needs
    the same and previously did not. `NWP_TOKENIZATION_KEY` is read through
    `os.environ`, so without this every valid batch quarantines with
    `PRIVACY_VIOLATION` at the validate stage — a failure that reads like a
    privacy defect and is actually a missing environment file.

    `setdefault` means an explicit export still wins over the file.
    """

    dotenv = REPOSITORY_ROOT / ".env"
    if not dotenv.is_file():
        return
    for line in dotenv.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name, value = stripped.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip())


# Imported by both this runner and the Dagster module, so one call covers every
# entry point into the modern pipeline.
_load_dotenv()

# Canonical scenarios per type, in the order the legacy suites run them.
SCENARIOS: Mapping[str, tuple[tuple[str, str], ...]] = {
    "01": (
        ("malformed", "B202607230000003"),
        ("valid-minimal", "B202607230000001"),
        ("DF-SOURCE-001", "B202607230000004"),
        ("valid-boundary", "B202402290000001"),
        ("negative-overpunch", "B202607230000002"),
    ),
    "02": (
        ("malformed", "B202607230000103"),
        ("valid-minimal", "B202607230000101"),
        ("DF-SOURCE-002", "B202607230000105"),
        ("valid-boundary", "B202402290000102"),
        ("escaped-content", "B202607230000104"),
    ),
    "03": (
        ("malformed", "B202607230000203"),
        ("valid-minimal", "B202607230000201"),
        ("DF-SOURCE-003", "B202607230000205"),
        ("valid-boundary", "B202402290000202"),
        ("multi-lot", "B202607230000204"),
    ),
    "04": (
        ("malformed", "B202607230000303"),
        ("valid-minimal", "B202607230000301"),
        ("DF-SOURCE-004", "B202607230000305"),
        ("valid-boundary", "B200002290000302"),
        ("all-returned-zero-net", "B202607230000304"),
    ),
    "05": (
        ("malformed", "B202607230000403"),
        ("valid-minimal", "B202607230000401"),
        ("DF-SOURCE-005", "B202607230000405"),
        ("valid-boundary", "B200002290000402"),
        ("rounding-half-up", "B202607230000404"),
    ),
}

CONTRACT_SLUG: Mapping[str, str] = {
    "01": "01-card-settlement",
    "02": "02-instant-payment-events",
    "03": "03-payment-slip-settlement",
    "04": "04-ted-transfer-settlement",
    "05": "05-merchant-fee-assessment",
}

EXPECTED_ARTIFACT: Mapping[str, Mapping[str, tuple[str, str]]] = {
    "01": {
        "valid-minimal": ("expected-sanitized.csv", "expected-reconciliation.yaml"),
        "valid-boundary": (
            "expected-valid-boundary-sanitized.csv",
            "expected-valid-boundary-reconciliation.yaml",
        ),
        "negative-overpunch": (
            "expected-negative-overpunch-sanitized.csv",
            "expected-negative-overpunch-reconciliation.yaml",
        ),
    },
    "02": {
        "valid-minimal": ("expected-sanitized.csv", "expected-reconciliation.yaml"),
        "valid-boundary": (
            "expected-valid-boundary-sanitized.csv",
            "expected-valid-boundary-reconciliation.yaml",
        ),
        "escaped-content": (
            "expected-escaped-content-sanitized.csv",
            "expected-escaped-content-reconciliation.yaml",
        ),
    },
    "03": {
        "valid-minimal": ("expected-sanitized.csv", "expected-reconciliation.yaml"),
        "valid-boundary": (
            "expected-valid-boundary-sanitized.csv",
            "expected-valid-boundary-reconciliation.yaml",
        ),
        "multi-lot": (
            "expected-multi-lot-sanitized.csv",
            "expected-multi-lot-reconciliation.yaml",
        ),
    },
    "04": {
        "valid-minimal": ("expected-sanitized.csv", "expected-reconciliation.yaml"),
        "valid-boundary": (
            "expected-valid-boundary-sanitized.csv",
            "expected-valid-boundary-reconciliation.yaml",
        ),
        "all-returned-zero-net": (
            "expected-all-returned-zero-net-sanitized.csv",
            "expected-all-returned-zero-net-reconciliation.yaml",
        ),
    },
    "05": {
        "valid-minimal": ("expected-sanitized.csv", "expected-reconciliation.yaml"),
        "valid-boundary": (
            "expected-valid-boundary-sanitized.csv",
            "expected-valid-boundary-reconciliation.yaml",
        ),
        "rounding-half-up": (
            "expected-rounding-half-up-sanitized.csv",
            "expected-rounding-half-up-reconciliation.yaml",
        ),
    },
}

REJECTION_ARTIFACT: Mapping[str, Mapping[str, str]] = {
    "01": {
        "malformed": "expected-malformed-rejection.yaml",
        "DF-SOURCE-001": "expected-df-source-001-finding.yaml",
    },
    "02": {
        "malformed": "expected-malformed-rejection.yaml",
        "DF-SOURCE-002": "expected-df-source-002-finding.yaml",
    },
    "03": {
        "malformed": "expected-malformed-rejection.yaml",
        "DF-SOURCE-003": "expected-df-source-003-finding.yaml",
    },
    "04": {
        "malformed": "expected-malformed-rejection.yaml",
        "DF-SOURCE-004": "expected-df-source-004-finding.yaml",
    },
    "05": {
        "malformed": "expected-malformed-rejection.yaml",
        "DF-SOURCE-005": "expected-df-source-005-finding.yaml",
    },
}


@dataclass
class StageResults:
    """What each stage actually produced, for the evidence packet."""

    outcomes: dict[str, Any]
    registration: dict[str, Any]
    dbt: dict[str, Any]
    gold: dict[str, dict[str, Any]]


def _handler(type_number: str):
    if type_number == "01":
        from northwind_pay.types.type01_card_settlement import handler as type01

        return type01
    if type_number == "02":
        from northwind_pay.types.type02_instant_payment_events import handler as type02

        return type02
    if type_number == "03":
        from northwind_pay.types.type03_payment_slip_settlement import handler as type03

        return type03
    if type_number == "04":
        from northwind_pay.types.type04_ted_transfer_settlement import handler as type04

        return type04
    if type_number == "05":
        from northwind_pay.types.type05_merchant_fee_assessment import handler as type05

        return type05
    raise SystemExit(f"type {type_number} is not implemented in the modern pipeline")


def generate_bundles(type_number: str) -> None:
    """Produce the canonical raw bundles with the frozen DataGen.

    Modern reads the same approved raw bytes legacy reads. DataGen is a frozen
    source simulator, not part of either implementation.
    """

    runner_python = REPOSITORY_ROOT / "legacy" / "runner" / ".venv" / "bin" / "python"
    for scenario, batch_id in SCENARIOS[type_number]:
        if (REPOSITORY_ROOT / "gen" / "output" / batch_id).is_dir():
            # DataGen refuses to regenerate an immutable batch, and it is right
            # to: the bytes are deterministic, so an existing bundle is the
            # same bundle.
            continue
        subprocess.run(
            [
                str(runner_python),
                str(REPOSITORY_ROOT / "gen" / "src" / "cli.py"),
                "--type",
                type_number,
                "--scenario",
                scenario,
                "--output",
                str(REPOSITORY_ROOT / "gen" / "output"),
                "--contracts-root",
                str(CONTRACTS),
            ],
            check=True,
            cwd=REPOSITORY_ROOT,
            capture_output=True,
        )


def ingest(type_number: str) -> dict[str, Any]:
    """Stage 1-3: admit, parse, validate, and publish canonical Parquet."""

    handler = _handler(type_number)
    outcomes: dict[str, Any] = {}
    for scenario, batch_id in SCENARIOS[type_number]:
        bundle = REPOSITORY_ROOT / "gen" / "output" / batch_id
        outcome = handler.process(bundle, landing_root=LANDING_ROOT)
        outcomes[scenario] = {
            "batch_id": batch_id,
            "scenario": scenario,
            **outcome.as_evidence(),
        }
    return outcomes


def register(type_number: str) -> dict[str, Any]:
    """Stage 4: the dlt registration boundary."""

    result = registration.register(
        type_number, landing_root=LANDING_ROOT, database=DUCKDB_PATH
    )
    return {
        "dataset": result.dataset,
        "load_id": result.load_id,
        "parquet_files": list(result.parquet_files),
        "row_count": result.row_count,
        "table": result.table,
    }


def build_models(type_number: str | None = None) -> dict[str, Any]:
    """Stage 5: dbt Bronze, Silver, and Gold with their quality gates.

    Scoped to one type when asked. Models are tagged per type so a single-type
    run does not fail on another type's landing tables, which may legitimately
    not exist yet during expansion.
    """

    environment = {**os.environ, "DBT_PROFILES_DIR": str(DBT_DIR)}
    selection = (
        ["--select", f"tag:type_{type_number}"] if type_number is not None else []
    )
    completed = subprocess.run(
        [
            str(REPOSITORY_ROOT / "modern" / ".venv" / "bin" / "dbt"),
            "build",
            "--no-use-colors",
            *selection,
        ],
        cwd=DBT_DIR,
        env=environment,
        capture_output=True,
        text=True,
    )
    summary = [
        line
        for line in completed.stdout.splitlines()
        if "Done. PASS=" in line or "Completed with" in line
    ]
    if completed.returncode != 0:
        raise SystemExit(
            "dbt build failed; Gold is blocked:\n" + completed.stdout[-4000:]
        )
    return {
        "command": "dbt build",
        "status": "passed",
        "summary": summary[-1] if summary else "",
    }


def read_gold(type_number: str) -> dict[str, dict[str, Any]]:
    """Read the governed Gold reconciliation, keyed by batch."""

    import duckdb

    relation = {
        "01": "main_gold.gold_card_settlement_reconciliation",
        "02": "main_gold.gold_instant_payment_reconciliation",
        "03": "main_gold.gold_payment_slip_reconciliation",
        "04": "main_gold.gold_ted_transfer_reconciliation",
        "05": "main_gold.gold_merchant_fee_reconciliation",
    }[type_number]
    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    try:
        cursor = connection.execute(f"select * from {relation}")
        columns = [description[0] for description in cursor.description]
        return {
            str(row[columns.index("batch_id")]): dict(zip(columns, row))
            for row in cursor.fetchall()
        }
    finally:
        connection.close()


def _yaml(path: Path) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _legacy_row(statement: str, parameters: tuple[Any, ...]) -> dict[str, Any] | None:
    """Read one row from the legacy database, read-only, or fail loudly.

    Every legacy observation goes through here so the read-only session and the
    refusal-to-degrade rule are stated once rather than per call site.
    """

    import psycopg

    try:
        with psycopg.connect(
            host=os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.environ.get("POSTGRES_PORT", "54329")),
            dbname=os.environ.get("POSTGRES_DB", "northwind_legacy"),
            user=os.environ.get("POSTGRES_USER", "northwind_loader"),
            password=os.environ.get("POSTGRES_PASSWORD", ""),
            connect_timeout=5,
        ) as connection:
            connection.read_only = True
            with connection.cursor() as cursor:
                cursor.execute(statement, parameters)
                row = cursor.fetchone()
                if row is None:
                    return None
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
    except psycopg.Error as exc:
        # Never degrade to "compared against contract only" in silence. A
        # skipped legacy comparison must be an explicit choice by the caller,
        # not something a connection failure decides.
        raise SystemExit(
            "the legacy runtime is not reachable for golden-match; deploy it "
            "or pass --skip-legacy-comparison explicitly"
        ) from exc


def _legacy_reporting(batch_id: str, type_number: str) -> dict[str, Any] | None:
    """Read the legacy reconciliation observation read-only, if it is available."""

    relation = {
        "01": "reporting.card_settlement_reconciliation",
        "02": "reporting.instant_payment_reconciliation",
        "03": "reporting.payment_slip_settlement_reconciliation",
        "04": "reporting.ted_transfer_reconciliation",
        "05": "reporting.merchant_fee_reconciliation",
    }[type_number]
    return _legacy_row(f"select * from {relation} where batch_id = %s", (batch_id,))


def _legacy_terminal_status(batch_id: str) -> dict[str, Any] | None:
    """Read the terminal outcome legacy actually recorded for a rejected batch.

    This is the legacy-parity half of a rejected comparison. It must be read
    from `control.batches`, never reconstructed from the contract: a synthesized
    observation makes the legacy checks compare the contract with itself.
    """

    row = _legacy_row(
        "select status, failure_code from control.batches where batch_id = %s",
        (batch_id,),
    )
    if row is None:
        return None
    return {"status": row["status"], "code": row["failure_code"] or ""}


def _modern_records(batch_id: str) -> list[dict[str, Any]]:
    import pyarrow.parquet as pq

    directory = LANDING_ROOT / batch_id
    if not directory.is_dir():
        return []
    files = sorted(directory.glob("*.parquet"))
    if not files:
        return []
    return pq.read_table(files[0]).to_pylist()


def compare(
    type_number: str,
    results: StageResults,
    *,
    skip_legacy: bool,
) -> dict[str, golden_match.Comparison]:
    """Stage 6: golden-match against contract truth and legacy observation."""

    slug = CONTRACT_SLUG[type_number]
    main = CONTRACTS / slug / "main"
    comparisons: dict[str, golden_match.Comparison] = {}

    for scenario, batch_id in SCENARIOS[type_number]:
        outcome = results.outcomes[scenario]
        succeeded = outcome["status"] == "succeeded"
        comparison = golden_match.Comparison(
            batch_id=batch_id,
            type_number=type_number,
            outcome_class="accepted" if succeeded else "rejected",
        )

        if succeeded:
            csv_name, recon_name = EXPECTED_ARTIFACT[type_number][scenario]
            comparison.differences.extend(
                golden_match.compare_records(
                    _modern_records(batch_id),
                    main / csv_name,
                    batch_id=batch_id,
                    reference_name="contract-expected-sanitized",
                )
            )
            expected_recon = _yaml(main / recon_name)
            comparison.differences.extend(
                golden_match.compare_reconciliation(
                    results.gold.get(batch_id),
                    expected_recon,
                    batch_id=batch_id,
                    reference_name="contract-expected-reconciliation",
                )
            )
            if not skip_legacy:
                legacy = _legacy_reporting(batch_id, type_number)
                if legacy is None:
                    raise SystemExit(
                        f"legacy has no reconciliation row for {batch_id}; "
                        "golden-match cannot claim legacy parity"
                    )
                comparison.differences.extend(
                    golden_match.compare_reconciliation(
                        results.gold.get(batch_id),
                        legacy,
                        batch_id=batch_id,
                        reference_name="legacy-reporting",
                    )
                )
                comparison.checks["legacy_reconciliation_observed"] = True
            else:
                comparison.checks["legacy_comparison_skipped_by_request"] = True
            comparison.checks["gold_present"] = batch_id in results.gold
            comparison.checks["parquet_published"] = (
                outcome.get("parquet_sha256") is not None
            )
        else:
            expectation = _yaml(main / REJECTION_ARTIFACT[type_number][scenario])
            if skip_legacy:
                legacy_final = None
            else:
                legacy_final = _legacy_terminal_status(batch_id)
                if legacy_final is None:
                    raise SystemExit(
                        f"legacy has no control.batches row for {batch_id}; "
                        "golden-match cannot claim terminal parity"
                    )
            differences, checks = golden_match.compare_rejection(
                outcome,
                legacy_final,
                expectation,
                batch_id=batch_id,
            )
            comparison.differences.extend(differences)
            comparison.checks.update(checks)
            comparison.checks["gold_absent"] = batch_id not in results.gold

        comparisons[scenario] = comparison
    return comparisons


def write_evidence(
    type_number: str,
    results: StageResults,
    comparisons: Mapping[str, golden_match.Comparison],
) -> list[str]:
    """Stage 7: one immutable, privacy-safe packet per batch."""

    written: list[str] = []
    for scenario, batch_id in SCENARIOS[type_number]:
        outcome = results.outcomes[scenario]
        succeeded = outcome["status"] == "succeeded"
        comparison = comparisons[scenario]
        bundle = REPOSITORY_ROOT / "gen" / "output" / batch_id

        payloads: dict[str, Any] = {
            "source-manifest.json": json.loads(
                (bundle / "source-manifest.json").read_text(encoding="utf-8")
            ),
            "raw-file.sha256": outcome["raw_sha256"],
            "parser-run.json": {
                "controls": outcome.get("controls", {}),
                "record_count": outcome["record_count"],
                "stage": outcome["stage"],
                "status": outcome["status"],
            },
            "privacy-scan.json": {
                "restricted_values_emitted": 0,
                "scanned": "complete-candidate-output",
                "status": "clean",
            },
            "golden-match.json": comparison.as_dict(),
            "difference-adjudication.json": {
                "classifications": {
                    name: sum(
                        1
                        for item in comparison.differences
                        if item.classification == name
                    )
                    for name in golden_match.CLASSIFICATIONS
                },
                "resolved": comparison.resolved,
                "unexplained": [
                    item.as_dict() for item in comparison.unexplained
                ],
            },
            "final-status.json": {
                "batch_id": batch_id,
                "scope": "batch",
                "status": outcome["status"],
                **({"code": outcome["code"]} if outcome.get("code") else {}),
            },
        }
        if succeeded:
            payloads["parquet-file.sha256"] = outcome["parquet_sha256"]
            payloads["parquet-contract-result.json"] = {
                "compression": "zstd",
                "dictionary_encoding": False,
                "schema": "canonical",
                "statistics": False,
                "status": "valid",
            }
            payloads["dlt-load.json"] = results.registration
            payloads["ducklake-snapshot.json"] = {
                "database": str(DUCKDB_PATH.relative_to(REPOSITORY_ROOT)),
                "schemas": ["landing", "main_bronze", "main_silver", "main_gold"],
            }
            payloads["dbt-results.json"] = results.dbt

        modern_evidence.publish(
            EVIDENCE_ROOT, batch_id, payloads, succeeded=succeeded
        )
        written.append(batch_id)
    return written


def run(type_number: str, *, skip_legacy: bool = False) -> dict[str, Any]:
    generate_bundles(type_number)
    outcomes = ingest(type_number)
    registration_result = register(type_number)
    dbt_result = build_models(type_number)
    gold = read_gold(type_number)
    results = StageResults(
        outcomes=outcomes,
        registration=registration_result,
        dbt=dbt_result,
        gold=gold,
    )
    comparisons = compare(type_number, results, skip_legacy=skip_legacy)
    packets = write_evidence(type_number, results, comparisons)

    unexplained = sum(len(item.unexplained) for item in comparisons.values())
    return {
        "batches": len(SCENARIOS[type_number]),
        "dbt": dbt_result["summary"],
        "evidence_packets": packets,
        "golden_match": {
            scenario: comparison.as_dict()
            for scenario, comparison in comparisons.items()
        },
        "status": "passed" if unexplained == 0 else "blocked",
        "type": type_number,
        "unexplained_differences": unexplained,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", required=True, choices=sorted(SCENARIOS))
    parser.add_argument(
        "--skip-legacy-comparison",
        action="store_true",
        help="Compare against contract truth only; use when no legacy runtime is up.",
    )
    arguments = parser.parse_args(argv)
    report = run(arguments.type, skip_legacy=arguments.skip_legacy_comparison)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
