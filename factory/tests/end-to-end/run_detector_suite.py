#!/usr/bin/env python3
"""Live Dark Factory acceptance for one type, or for all five.

Runs against a deployed legacy runtime that has already produced its canonical
observations. It executes each of the six build-sequence gates as a probe rather
than asserting them in prose:

  Step 1  the finding validates against the frozen closed contract
  Step 2  every observation is read-only and lineage-bound
  Step 3  identical observations produce byte-identical canonical findings
  Step 4  withholding any required channel prevents a conclusive attribution
  Step 5  isolation and peer continuation are both observed
  Step 6  a fresh run recreates the expected packet with no leak or mutation

Usage:
    run_detector_suite.py --type 01|02|03|04|05|all \\
        --legacy-evidence-root <path>[,<path>...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY_ROOT / "factory" / "src"))

import cli  # noqa: E402
import contracts as contract_loader  # noqa: E402
from canonical import (  # noqa: E402
    encode,
    fixture_projection,
    identity_bytes,
)
from detector_config import DetectorConfiguration  # noqa: E402
from errors import (  # noqa: E402
    AttributionInconclusiveError,
    DarkFactoryError,
)
from findings import privacy  # noqa: E402
from findings import writer as finding_writer  # noqa: E402
from observations import postgres as postgres_adapter  # noqa: E402
from observations import transport as transport_adapter  # noqa: E402
from observations.collect import WITHHOLDABLE_CHANNELS  # noqa: E402

TYPES = ("01", "02", "03", "04", "05")


class AcceptanceFailure(AssertionError):
    """One acceptance probe did not hold."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AcceptanceFailure(message)


def _step1_contract(finding: Mapping[str, Any], scenario_name: str) -> None:
    contract = contract_loader.load()
    scenario = contract.scenarios[scenario_name]
    finding_writer.validate_schema(finding, contract.schema)
    expected = json.loads(
        contract_loader.expected_finding_path(scenario_name).read_text(
            encoding="utf-8"
        )
    )
    observed = fixture_projection(finding)
    _require(
        observed == expected,
        f"{scenario_name}: finding drifted from the frozen expected contract",
    )
    oracle_digest = hashlib.sha256(scenario.contract_oracle.read_bytes()).hexdigest()
    _require(
        finding["references"]["contract_oracle_sha256"] == f"sha256:{oracle_digest}",
        f"{scenario_name}: finding is not bound to the frozen legacy oracle",
    )


def _step2_lineage(finding: Mapping[str, Any], scenario_name: str) -> None:
    contract = contract_loader.load()
    scenario = contract.scenarios[scenario_name]
    configuration = DetectorConfiguration.load()
    with postgres_adapter.read_only_session(configuration) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT source_sha256, source_manifest_sha256 "
                "FROM control.batches WHERE batch_id = %s",
                (scenario.batch_id,),
            )
            row = cursor.fetchone()
    _require(row is not None, f"{scenario_name}: no live control-plane record")
    assert row is not None
    _require(
        finding["references"]["raw_sha256"] == f"sha256:{row[0]}",
        f"{scenario_name}: raw hash is not bound to the live control plane",
    )
    _require(
        finding["references"]["source_manifest_sha256"] == f"sha256:{row[1]}",
        f"{scenario_name}: manifest hash is not bound to the live control plane",
    )
    _require(
        len(finding["observations"]) >= 4,
        f"{scenario_name}: fewer than four observation channels were consumed",
    )
    independence = {
        entry["channel"]: entry["independence"] for entry in finding["observations"]
    }
    _require(
        independence["legacy-java-processor"] == "independent_computation",
        f"{scenario_name}: the processor channel lost its independence class",
    )


def _step3_byte_stability(
    scenario_name: str,
    type_number: str,
    legacy_evidence_root: Path,
    first: Mapping[str, Any],
) -> None:
    """Two runs over the same immutable observations must be byte-identical."""

    with tempfile.TemporaryDirectory() as temporary:
        second = cli.run(
            type_number,
            legacy_evidence_root=legacy_evidence_root,
            evidence_root=Path(temporary),
            publish=False,
        )
    _require(
        identity_bytes(first) == identity_bytes(second),
        f"{scenario_name}: repeated detection produced different canonical bytes",
    )
    _require(
        first["finding_id"] == second["finding_id"],
        f"{scenario_name}: repeated detection produced a different identity",
    )
    recomputed = encode(
        {key: value for key, value in first.items() if key != "finding_id"}
    )
    _require(
        len(recomputed) > 0 and first["finding_id"].startswith("sha256:"),
        f"{scenario_name}: finding identity is not a prefixed digest",
    )


def _step4_withhold(
    scenario_name: str,
    type_number: str,
    legacy_evidence_root: Path,
) -> list[str]:
    """Removing any required observation must prevent a conclusive attribution."""

    proven: list[str] = []
    for channel in WITHHOLDABLE_CHANNELS:
        try:
            with tempfile.TemporaryDirectory() as temporary:
                cli.run(
                    type_number,
                    legacy_evidence_root=legacy_evidence_root,
                    evidence_root=Path(temporary),
                    withhold=frozenset({channel}),
                    publish=False,
                )
        except AttributionInconclusiveError:
            proven.append(channel)
            continue
        except DarkFactoryError as error:
            raise AcceptanceFailure(
                f"{scenario_name}: withholding {channel} failed with {error} "
                "instead of an inconclusive attribution"
            ) from error
        raise AcceptanceFailure(
            f"{scenario_name}: withholding {channel} still produced a "
            "conclusive attribution, so the channel is not required"
        )
    return proven


def _step5_isolation_and_continuation(
    finding: Mapping[str, Any],
    scenario_name: str,
) -> None:
    contract = contract_loader.load()
    scenario = contract.scenarios[scenario_name]
    configuration = DetectorConfiguration.load()

    isolation = finding["isolation"]
    _require(isolation["observed"], f"{scenario_name}: isolation was not observed")
    _require(
        not isolation["sanitized_csv_present"],
        f"{scenario_name}: sanitized output exists for a quarantined batch",
    )
    _require(
        isolation["raw_quarantine_present"],
        f"{scenario_name}: the raw quarantine bundle is missing",
    )
    _require(
        isolation["staging_row_count"] == 0
        and isolation["business_row_count"] == 0,
        f"{scenario_name}: the quarantined batch has business rows",
    )
    _require(
        not isolation["postgres_business_mutation"],
        f"{scenario_name}: PostgreSQL business state was mutated",
    )
    _require(
        isolation["quarantine_scope"] == "batch",
        f"{scenario_name}: quarantine is not batch-scoped",
    )

    # Independently reconfirm isolation against the live runtime rather than
    # trusting the finding's own summary of it.
    with transport_adapter.read_only_transport(configuration) as channel:
        live = transport_adapter.observe_transport(
            channel, batch_id=scenario.batch_id
        )
    _require(
        not live.sanitized_csv_present and live.raw_quarantine_present,
        f"{scenario_name}: live transport disagrees with the finding",
    )

    continuation = finding["continuation"]
    _require(
        continuation["observed"],
        f"{scenario_name}: peer continuation was not observed",
    )
    observed_peers = [peer["batch_id"] for peer in continuation["peers"]]
    _require(
        observed_peers == list(scenario.required_peers),
        f"{scenario_name}: the finding does not name the required peers",
    )
    for peer in continuation["peers"]:
        _require(
            peer["status"] == "succeeded"
            and peer["reconciliation_status"] == "MATCHED",
            f"{scenario_name}: peer {peer['batch_id']} did not reconcile",
        )


def _step6_packet(
    scenario_name: str,
    type_number: str,
    legacy_evidence_root: Path,
    evidence_root: Path,
) -> Path:
    contract = contract_loader.load()
    scenario = contract.scenarios[scenario_name]
    finding = cli.run(
        type_number,
        legacy_evidence_root=legacy_evidence_root,
        evidence_root=evidence_root,
        publish=True,
    )
    packet = evidence_root.resolve() / scenario.batch_id
    _require(packet.is_dir(), f"{scenario_name}: no evidence packet was published")
    _require(
        sorted(path.name for path in packet.iterdir())
        == sorted(finding_writer.PACKET_FILES),
        f"{scenario_name}: the evidence packet is incomplete",
    )
    _require(
        packet.stat().st_mode & 0o777 == 0o700,
        f"{scenario_name}: the evidence packet is not private",
    )
    published = json.loads((packet / "finding.json").read_text(encoding="utf-8"))
    _require(
        published["finding_id"] == finding["finding_id"],
        f"{scenario_name}: the published finding is not the detected one",
    )

    # No restricted identifier may appear anywhere in the packet, not only in
    # the finding, so the whole packet is scanned as published bytes.
    tokens = privacy.extract_restricted_digits(
        scenario.raw_fixture, scenario.raw_encoding, contract.allowlist
    )
    exempt = privacy.structural_digits(
        (scenario.batch_id, *scenario.required_peers)
    )
    for path in sorted(packet.iterdir()):
        document = json.loads(path.read_text(encoding="utf-8"))
        haystack = privacy.scannable_text(document, contract.allowlist)
        for token in tokens:
            if any(token in identity for identity in exempt):
                continue
            _require(
                token not in haystack,
                f"{scenario_name}: a restricted identifier reached {path.name}",
            )
    return packet


def _legacy_untouched(before: Mapping[str, str], after: Mapping[str, str]) -> None:
    changed = sorted(
        name for name, digest in after.items() if before.get(name) != digest
    )
    _require(
        not changed,
        "the detector mutated legacy evidence: " + ", ".join(changed),
    )


def _digest_tree(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def run_type(
    type_number: str,
    legacy_evidence_root: Path,
    evidence_root: Path,
) -> dict[str, Any]:
    contract = contract_loader.load()
    scenario = contract.for_type(type_number)
    name = scenario.scenario

    before = _digest_tree(legacy_evidence_root)

    with tempfile.TemporaryDirectory() as temporary:
        finding = cli.run(
            type_number,
            legacy_evidence_root=legacy_evidence_root,
            evidence_root=Path(temporary),
            publish=False,
        )

    _step1_contract(finding, name)
    _step2_lineage(finding, name)
    _step3_byte_stability(name, type_number, legacy_evidence_root, finding)
    withheld = _step4_withhold(name, type_number, legacy_evidence_root)
    _step5_isolation_and_continuation(finding, name)
    packet = _step6_packet(name, type_number, legacy_evidence_root, evidence_root)

    _legacy_untouched(before, _digest_tree(legacy_evidence_root))

    return {
        "batch_id": scenario.batch_id,
        "byte_stable": True,
        "evidence_packet": str(packet.relative_to(REPOSITORY_ROOT)),
        "finding_id": finding["finding_id"],
        "isolation": "verified",
        "legacy_evidence_unchanged": True,
        "peer_continuation": "verified",
        "privacy": "clean",
        "required_channels_proven": sorted(withheld),
        "scenario": name,
        "status": "passed",
        "type": type_number,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", required=True, choices=(*TYPES, "all"))
    parser.add_argument(
        "--legacy-evidence-root",
        required=True,
        help=(
            "Legacy evidence root. For TYPE=all, pass one root per type as a "
            "comma-separated list in type order."
        ),
    )
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=REPOSITORY_ROOT / "evidence" / "factory",
    )
    arguments = parser.parse_args(argv)

    roots = [Path(part) for part in arguments.legacy_evidence_root.split(",")]
    selected = TYPES if arguments.type == "all" else (arguments.type,)
    if len(roots) == 1:
        roots = roots * len(selected)
    if len(roots) != len(selected):
        print(
            "provide one legacy evidence root per selected type",
            file=sys.stderr,
        )
        return 2

    results = []
    for type_number, root in zip(selected, roots):
        try:
            results.append(run_type(type_number, root, arguments.evidence_root))
        except (AcceptanceFailure, DarkFactoryError) as error:
            print(f"Dark Factory acceptance failed: {error}", file=sys.stderr)
            return 1
        print(f"Type {type_number} Dark Factory acceptance passed")

    print(
        json.dumps(
            {
                "detector_version": contract_loader.load().detector_version,
                "results": results,
                "status": "passed",
                "types": list(selected),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
