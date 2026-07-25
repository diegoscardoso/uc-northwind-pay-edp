"""Unit proof for the modern Type 05 ingestion.

Three things are worth testing here and one of them is worth testing twice: the
locale-aware lexer, the quoting rules the contract binds per position, and the
HALF_UP rounding that a default `round()` would silently get wrong.
"""

from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "modern" / "ingestion" / "src"))

MAIN = REPOSITORY_ROOT / "contracts" / "types" / "05-merchant-fee-assessment" / "main"

from northwind_pay.types.type05_merchant_fee_assessment import (  # noqa: E402
    parser,
    schema,
)
from northwind_pay.types.type05_merchant_fee_assessment.model import (  # noqa: E402
    Assessment,
)

DECLARED = {
    "row_count": 2,
    "gross_amount": "1001.00",
    "assessed_fee": "12.36",
    "calculated_fee": "12.36",
    "currency": "BRL",
}


def _assessment(gross: str, rate: str, assessed: str) -> Assessment:
    from datetime import date

    return Assessment(
        physical_record_number=2,
        assessment_id="FEE2026072304001",
        batch_id="B202607230000401",
        merchant_id="MER0000000000001",
        merchant_tax_id="12345678000195",
        fee_code="MDR",
        description="x",
        gross_amount_brl=Decimal(gross),
        rate_percent=Decimal(rate),
        assessed_fee_brl=Decimal(assessed),
        assessment_date=date(2026, 7, 23),
    )


class RoundingTest(unittest.TestCase):
    """The contract says HALF_UP. Python's default says otherwise."""

    def test_half_up_rounds_a_tie_away_from_zero(self) -> None:
        # 1.00 * 0.500% = 0.005 exactly. HALF_UP gives 0.01; banker's rounding
        # gives 0.00, and every structural test would still pass.
        self.assertEqual(
            parser.calculated_fee(_assessment("1.00", "0.500", "0.01")),
            Decimal("0.01"),
        )

    def test_it_is_not_bankers_rounding(self) -> None:
        """Pin the difference so a later refactor cannot reintroduce HALF_EVEN.

        The exact product here is 0.005 — a true tie. Banker's rounding goes to
        the even digit and yields 0.00; the contract requires 0.01. Every
        structural test passes either way, which is exactly why this one exists.
        """

        from decimal import ROUND_HALF_EVEN

        exact = Decimal("1.00") * Decimal("0.500") / Decimal(100)
        bankers = exact.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        self.assertEqual(bankers, Decimal("0.00"))
        self.assertEqual(
            parser.calculated_fee(_assessment("1.00", "0.500", "0.01")),
            Decimal("0.01"),
        )

    def test_an_exact_product_is_untouched(self) -> None:
        self.assertEqual(
            parser.calculated_fee(_assessment("1000.00", "1.235", "12.35")),
            Decimal("12.35"),
        )


class LexerTest(unittest.TestCase):
    def test_a_semicolon_inside_quotes_is_content(self) -> None:
        parsed = parser.parse(
            (MAIN / "valid-minimal.csv").read_bytes(), declared_controls=DECLARED
        )
        self.assertEqual(parsed.assessments[0].description, 'Tarifa "VIP"; julho, lote A')

    def test_computed_controls_are_independent_of_the_declaration(self) -> None:
        parsed = parser.parse(
            (MAIN / "valid-minimal.csv").read_bytes(), declared_controls=DECLARED
        )
        self.assertEqual(parsed.computed_row_count, 2)
        self.assertEqual(parsed.computed_assessed_fee, Decimal("12.36"))
        self.assertEqual(parsed.computed_calculated_fee, Decimal("12.36"))

    def test_an_unquoted_description_is_refused(self) -> None:
        """The contract binds quoting per position, not per taste."""

        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                (MAIN / "malformed.csv").read_bytes(), declared_controls=DECLARED
            )
        self.assertEqual(caught.exception.code, "INVALID_CSV_QUOTING")

    def test_a_carriage_return_is_refused(self) -> None:
        payload = (MAIN / "valid-minimal.csv").read_bytes().replace(b"\n", b"\r\n")
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(payload, declared_controls=DECLARED)
        self.assertEqual(caught.exception.code, "INVALID_LINE_ENDING")


class SourceDefectTest(unittest.TestCase):
    """The declaration is confronted, never repaired."""

    def test_a_contradicted_declaration_is_refused_and_preserved(self) -> None:
        declared = dict(DECLARED)
        declared["assessed_fee"] = "12.35"  # the source is one cent short
        parsed = parser.parse(
            (MAIN / "valid-minimal.csv").read_bytes(), declared_controls=declared
        )
        with self.assertRaises(schema.SchemaError) as caught:
            schema.sanitize(parsed, source_filename="NW_MERCHANT_FEES_x.csv")
        self.assertEqual(
            caught.exception.code, "SOURCE_CONTROL_ASSESSED_FEE_MISMATCH"
        )
        controls = schema.controls_of(parsed).as_evidence()
        self.assertEqual(controls["declared_assessed_fee"], "12.35")
        self.assertEqual(controls["computed_assessed_fee"], "12.36")


class PrivacyTest(unittest.TestCase):
    def test_the_tax_identifier_is_masked_and_never_emitted_clear(self) -> None:
        parsed = parser.parse(
            (MAIN / "valid-minimal.csv").read_bytes(), declared_controls=DECLARED
        )
        sanitized = schema.sanitize(parsed, source_filename="NW_MERCHANT_FEES_x.csv")
        for record in sanitized.records:
            self.assertRegex(record.merchant_tax_id_masked, r"^\*{10}[0-9]{4}$")
        emitted = " ".join(r.merchant_tax_id_masked for r in sanitized.records)
        for item in parsed.assessments:
            self.assertNotIn(item.merchant_tax_id, emitted)


class WriterTest(unittest.TestCase):
    def test_the_rate_keeps_its_own_scale(self) -> None:
        from northwind_pay.types.type05_merchant_fee_assessment import writer

        fields = dict(writer.SCHEMA_FIELDS)
        self.assertEqual(str(fields["rate_percent"]), "decimal128(9, 3)")
        self.assertEqual(str(fields["assessed_fee_brl"]), "decimal128(18, 2)")


if __name__ == "__main__":
    unittest.main()
