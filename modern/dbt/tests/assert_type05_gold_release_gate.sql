{{ config(tags=['type_05']) }}

-- Type 05 release gate. Every delta column in this Gold is genuinely
-- computed, so all five belong here; only `reject_count` is a constant and is
-- deliberately excluded. See modern/README.md, "Constant columns in Gold".

{{ release_gate(ref('gold_merchant_fee_reconciliation'), [
    'count_delta',
    'gross_amount_delta',
    'assessed_fee_delta',
    'calculated_fee_delta',
    'assessment_calculation_delta',
]) }}
