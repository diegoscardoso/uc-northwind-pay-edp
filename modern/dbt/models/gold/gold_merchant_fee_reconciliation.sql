{{ config(tags=['type_05']) }}

-- Gold: governed Type 05 reconciliation, one row per (batch_id, currency).
-- Columns and deltas mirror the legacy reporting grain exactly.
--
-- CONSTANT COLUMNS: `gross_amount_delta`, `calculated_fee_delta`, and
-- `reject_count` are literals, and `source_gross_amount` / `source_calculated_fee`
-- are aliases of their `staged_*` counterparts. They exist so the grain matches
-- the legacy report. Never assert on them. Real deltas are `count_delta`,
-- `assessed_fee_delta`, and `assessment_calculation_delta` — the last being the
-- HALF_UP rounding proof.

with control as (
    select * from {{ ref('bronze_merchant_fee_control') }}
),

staged as (
    select
        batch_id,
        count(*)                                          as staged_count,
        coalesce(sum(gross_amount_brl), 0.00)             as staged_gross_amount,
        coalesce(sum(assessed_fee_brl), 0.00)             as staged_assessed_fee,
        coalesce(sum(calculated_fee_brl), 0.00)           as staged_calculated_fee
    from {{ ref('bronze_merchant_fee_assessment') }}
    group by batch_id
),

applied as (
    select
        batch_id,
        count(*)                                          as applied_count,
        coalesce(sum(gross_amount_brl), 0.00)             as applied_gross_amount,
        coalesce(sum(assessed_fee_brl), 0.00)             as applied_assessed_fee,
        coalesce(sum(calculated_fee_brl), 0.00)           as applied_calculated_fee,
        coalesce(sum(assessment_calculation_delta), 0.00) as assessment_calculation_delta
    from {{ ref('silver_merchant_fee_assessment') }}
    group by batch_id
)

select
    control.batch_id,
    control.currency,
    control.declared_row_count                                      as source_count,
    staged.staged_count,
    applied.applied_count,
    cast(staged.staged_gross_amount as decimal(18, 2))              as source_gross_amount,
    cast(staged.staged_gross_amount as decimal(18, 2))              as staged_gross_amount,
    cast(applied.applied_gross_amount as decimal(18, 2))            as applied_gross_amount,
    control.declared_assessed_fee                                   as source_assessed_fee,
    cast(staged.staged_assessed_fee as decimal(18, 2))              as staged_assessed_fee,
    cast(applied.applied_assessed_fee as decimal(18, 2))            as applied_assessed_fee,
    cast(staged.staged_calculated_fee as decimal(18, 2))            as source_calculated_fee,
    cast(staged.staged_calculated_fee as decimal(18, 2))            as staged_calculated_fee,
    cast(applied.applied_calculated_fee as decimal(18, 2))          as applied_calculated_fee,
    applied.applied_count - control.declared_row_count              as count_delta,
    cast(0.00 as decimal(18, 2))                                    as gross_amount_delta,
    cast(
        applied.applied_assessed_fee - control.declared_assessed_fee
        as decimal(18, 2)
    )                                                               as assessed_fee_delta,
    cast(0.00 as decimal(18, 2))                                    as calculated_fee_delta,
    cast(applied.assessment_calculation_delta as decimal(18, 2))    as assessment_calculation_delta,
    0                                                               as reject_count,
    case
        when applied.applied_count = control.declared_row_count
         and applied.applied_assessed_fee = control.declared_assessed_fee
         and applied.assessment_calculation_delta = 0.00
        then 'MATCHED'
        else 'MISMATCHED'
    end                                                             as status
from control
join staged  on staged.batch_id  = control.batch_id
join applied on applied.batch_id = control.batch_id
