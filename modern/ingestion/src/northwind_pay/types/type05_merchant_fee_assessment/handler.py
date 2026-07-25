"""Compose admission, parsing, schema, and publication for one Type 05 batch."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...common.money import render
from ...common.parquet import publish
from ...common.privacy import PrivacyError
from ...intake.admission import AdmissionError, admit
from ..type01_card_settlement.handler import BatchOutcome
from . import parser, writer
from .schema import SchemaError, controls_of, sanitize

TYPE_NUMBER = "05"


def _quarantined(
    batch_id: str,
    *,
    code: str,
    stage: str,
    raw_sha256: str,
    controls: dict[str, Any],
) -> BatchOutcome:
    return BatchOutcome(
        batch_id=batch_id,
        type_number=TYPE_NUMBER,
        status="quarantined",
        code=code,
        stage=stage,
        raw_sha256=raw_sha256,
        parquet_sha256=None,
        record_count=0,
        controls=controls,
    )


def process(bundle: Path, *, landing_root: Path) -> BatchOutcome:
    try:
        source = admit(bundle, expected_type=TYPE_NUMBER)
    except AdmissionError as error:
        return _quarantined(
            bundle.name, code=error.code, stage="intake", raw_sha256="", controls={}
        )

    try:
        parsed = parser.parse(
            source.payload, declared_controls=source.declared_controls
        )
    except parser.ParseError as error:
        return _quarantined(
            source.batch_id,
            code=error.code,
            stage="parse",
            raw_sha256=source.raw_sha256,
            controls={},
        )

    controls = controls_of(parsed)
    try:
        sanitized = sanitize(parsed, source_filename=source.source_filename)
    except SchemaError as error:
        return _quarantined(
            source.batch_id,
            code=error.code,
            stage="validate",
            raw_sha256=source.raw_sha256,
            controls=controls.as_evidence(),
        )
    except PrivacyError:
        return _quarantined(
            source.batch_id,
            code="PRIVACY_OUTPUT_VIOLATION",
            stage="validate",
            raw_sha256=source.raw_sha256,
            controls=controls.as_evidence(),
        )

    parquet_name = source.source_filename.replace(".csv", ".parquet")
    table = writer.table(
        sanitized.records, batch_id=sanitized.batch_id, raw_sha256=source.raw_sha256
    )
    result = publish(
        table,
        directory=landing_root,
        filename=parquet_name,
        manifest={
            "batch_id": sanitized.batch_id,
            # dlt's control extractor is generic across types and reads
            # `detail_count` / `net_amount`. Type 05's countable unit is the
            # assessment row and its governed total is the assessed fee, so
            # they travel under those names and Bronze aliases them back.
            "computed_assessed_fee": render(controls.computed_assessed_fee),
            "computed_detail_count": controls.computed_row_count,
            "computed_net_amount": render(controls.computed_assessed_fee),
            "computed_calculated_fee": render(controls.computed_calculated_fee),
            "computed_gross_amount": render(controls.computed_gross_amount),
            "computed_row_count": controls.computed_row_count,
            "contract_code": source.contract_code,
            "contract_version": source.contract_version,
            "currency": controls.currency,
            "declared_assessed_fee": render(controls.declared_assessed_fee),
            "declared_detail_count": controls.declared_row_count,
            "declared_net_amount": render(controls.declared_assessed_fee),
            "declared_calculated_fee": render(controls.declared_calculated_fee),
            "declared_gross_amount": render(controls.declared_gross_amount),
            "declared_row_count": controls.declared_row_count,
            "layout_version": source.layout_version,
            "parquet_file": parquet_name,
            "raw_sha256": source.raw_sha256,
            "record_count": len(sanitized.records),
            "source_file": source.source_filename,
            "source_manifest_sha256": source.manifest_sha256,
            "type_number": TYPE_NUMBER,
            "writer_version": writer.WRITER_VERSION,
        },
    )
    return BatchOutcome(
        batch_id=sanitized.batch_id,
        type_number=TYPE_NUMBER,
        status="succeeded",
        code=None,
        stage="published",
        raw_sha256=source.raw_sha256,
        parquet_sha256=result["parquet_sha256"],
        record_count=len(sanitized.records),
        controls=controls.as_evidence(),
    )
