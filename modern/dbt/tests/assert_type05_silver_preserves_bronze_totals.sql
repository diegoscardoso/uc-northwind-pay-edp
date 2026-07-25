{{ config(tags=['type_05']) }}

{{ conserves_totals(
    ref('bronze_merchant_fee_assessment'),
    ref('silver_merchant_fee_assessment'),
    ['gross_amount_brl', 'assessed_fee_brl', 'calculated_fee_brl'],
) }}
