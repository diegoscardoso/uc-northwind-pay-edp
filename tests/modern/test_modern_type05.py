"""Modern Type 05 tests: lexing, HALF_UP, controls, privacy, and refusals."""

from __future__ import annotations

import unittest
from decimal import Decimal
from pathlib import Path
from typing import Any

from northwind_pay.types.type05_merchant_fee_assessment import parser, schema

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TYPE05 = REPOSITORY_ROOT / "contracts" / "types" / "05-merchant-fee-assessment" / "main"

VALID_MINIMAL_DECLARED: dict[str, Any] = {
    "row_count": 2,
    "gross_amount": "1001.00",
    "assessed_fee": "12.36",
    "calculated_fee": "12.36",
}


def _parse(name: str, batch_id: str, date: str = "20260723") -> parser.ParsedBatch:
    return parser.parse(
        (TYPE05 / f"{name}.csv").read_bytes(),
        source_filename=f"NW_MERCHANT_FEES_{date}_{batch_id}.csv",
    )


class Type05ParserTest(unittest.TestCase):
    def test_parses_the_minimal_batch(self) -> None:
        parsed = _parse("valid-minimal", "B202607230000401")
        self.assertEqual(parsed.computed_row_count, 2)
        self.assertEqual(parsed.computed_gross_amount, Decimal("1001.00"))
        self.assertEqual(parsed.computed_assessed_fee, Decimal("12.36"))
        self.assertEqual(parsed.computed_calculated_fee, Decimal("12.36"))

    def test_lexer_handles_escaped_quotes_and_inner_semicolons(self) -> None:
        parsed = _parse("valid-minimal", "B202607230000401")
        self.assertEqual(parsed.rows[0].description, 'Tarifa "VIP"; julho, lote A')

    def test_half_up_rounds_both_ties_upward(self) -> None:
        parsed = _parse("rounding-half-up", "B202607230000404")
        # 1,00 x 0,500% = 0.005 and 2,50 x 1,000% = 0.025: banker's rounding
        # would produce 0.00 and 0.02; the contract requires 0.01 and 0.03.
        self.assertEqual(parsed.rows[0].calculated_fee, Decimal("0.01"))
        self.assertEqual(parsed.rows[1].calculated_fee, Decimal("0.03"))
        self.assertEqual(parsed.computed_assessed_fee, Decimal("0.04"))

    def test_boundary_batch_parses_at_full_scale(self) -> None:
        parsed = _parse("valid-boundary", "B200002290000402", date="20000229")
        row = parsed.rows[0]
        self.assertEqual(row.gross_amount, Decimal("999999999999.99"))
        self.assertEqual(row.rate_percent, Decimal("100.000"))
        self.assertEqual(row.calculated_fee, Decimal("999999999999.99"))
        self.assertEqual(len(row.description), 80)

    def test_rejects_the_malformed_batch_for_quoting(self) -> None:
        with self.assertRaises(parser.ParseError) as caught:
            _parse("malformed", "B202607230000403")
        self.assertEqual(caught.exception.code, "INVALID_CSV_QUOTING")

    def test_rejects_a_wrong_row_level_fee(self) -> None:
        payload = (
            (TYPE05 / "valid-minimal.csv")
            .read_text(encoding="utf-8")
            .replace("12,35", "12,34")
            .encode("utf-8")
        )
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            )
        self.assertEqual(caught.exception.code, "FEE_CALCULATION_MISMATCH")

    def test_rejects_an_invalid_check_digit(self) -> None:
        payload = (
            (TYPE05 / "valid-minimal.csv")
            .read_text(encoding="utf-8")
            .replace("12345678000195", "12345678000194")
            .encode("utf-8")
        )
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            )
        self.assertEqual(caught.exception.code, "INVALID_DOCUMENT")

    def test_rejects_a_date_that_contradicts_the_filename(self) -> None:
        with self.assertRaises(parser.ParseError) as caught:
            _parse("valid-minimal", "B202607230000401", date="20260724")
        self.assertEqual(caught.exception.code, "INVALID_BUSINESS_DATE")

    def test_rejects_a_missing_final_newline(self) -> None:
        payload = (TYPE05 / "valid-minimal.csv").read_bytes().rstrip(b"\n")
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            )
        self.assertEqual(caught.exception.code, "INVALID_TRANSPORT")

    def test_rejects_a_duplicate_assessment_identity(self) -> None:
        text = (TYPE05 / "valid-minimal.csv").read_text(encoding="utf-8")
        lines = text.splitlines()
        duplicated = lines[1].replace("MER0000000000001", "MER0000000000002")
        payload = "\n".join([*lines, duplicated]).encode("utf-8") + b"\n"
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            )
        self.assertEqual(caught.exception.code, "DUPLICATE_IDENTIFIER")


class Type05SchemaTest(unittest.TestCase):
    def test_sanitizes_to_the_contract_shape(self) -> None:
        parsed = _parse("valid-minimal", "B202607230000401")
        sanitized = schema.sanitize(
            parsed,
            source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            declared=VALID_MINIMAL_DECLARED,
        )
        first = sanitized.records[0]
        self.assertEqual(first.source_record_number, 2)
        self.assertEqual(first.merchant_tax_id_masked, "**********0195")
        self.assertEqual(first.assessment_date, "2026-07-23")
        self.assertEqual(first.rounding_mode, "HALF_UP")
        self.assertEqual(first.assessed_fee_brl, first.calculated_fee_brl)

    def test_no_raw_cnpj_survives_into_the_candidate_output(self) -> None:
        parsed = _parse("valid-minimal", "B202607230000401")
        sanitized = schema.sanitize(
            parsed,
            source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            declared=VALID_MINIMAL_DECLARED,
        )
        payload = "\n".join(
            f"{record.merchant_tax_id_masked},{record.description}"
            for record in sanitized.records
        )
        self.assertNotIn("12345678000195", payload)
        self.assertNotIn("98765432000198", payload)

    def test_preserves_a_wrong_declaration_and_refuses(self) -> None:
        parsed = _parse("df-source-005", "B202607230000405")
        declared = {
            "row_count": 1,
            "gross_amount": "100.00",
            "assessed_fee": "0.99",
            "calculated_fee": "1.00",
        }
        controls = schema.controls_of(parsed, declared)
        self.assertEqual(controls.declared_assessed_fee, Decimal("0.99"))
        self.assertEqual(controls.computed_assessed_fee, Decimal("1.00"))
        with self.assertRaises(schema.SchemaError) as caught:
            schema.sanitize(
                parsed,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000405.csv",
                declared=declared,
            )
        self.assertEqual(
            caught.exception.code, "SOURCE_CONTROL_ASSESSED_FEE_MISMATCH"
        )
        evidence = controls.as_evidence()
        self.assertEqual(evidence["declared_assessed_fee"], "0.99")
        self.assertEqual(evidence["computed_assessed_fee"], "1.00")

    def test_refuses_a_wrong_declared_count(self) -> None:
        parsed = _parse("valid-minimal", "B202607230000401")
        with self.assertRaises(schema.SchemaError) as caught:
            schema.sanitize(
                parsed,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
                declared={**VALID_MINIMAL_DECLARED, "row_count": 3},
            )
        self.assertEqual(caught.exception.code, "SOURCE_CONTROL_COUNT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
