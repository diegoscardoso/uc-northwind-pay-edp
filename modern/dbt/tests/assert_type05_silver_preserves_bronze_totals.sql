{{ config(tags=['type_05']) }}

-- Silver derives `assessment_calculation_delta` from the two fee columns, so
-- both must be conserved for that derivation to mean anything.

{{ conserves_totals(
    ref('bronze_merchant_fee_assessment'),
    ref('silver_merchant_fee_assessment'),
    ['gross_amount_brl', 'assessed_fee_brl', 'calculated_fee_brl']
) }}
