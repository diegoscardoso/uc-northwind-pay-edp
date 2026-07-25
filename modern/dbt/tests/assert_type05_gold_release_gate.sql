{{ config(tags=['type_05']) }}

-- Type 05 release gate. `gross_amount_delta`, `calculated_fee_delta`, and
-- `reject_count` are constants and are deliberately excluded; see
-- modern/README.md, "Constant columns in Gold". `assessment_calculation_delta`
-- is a real computed column and is included: it is the HALF_UP rounding proof.

{{ release_gate(
    ref('gold_merchant_fee_reconciliation'),
    ['count_delta', 'assessed_fee_delta', 'assessment_calculation_delta']
) }}
