{{ config(tags=['type_05']) }}

-- Gold: governed Type 05 reconciliation, one row per (batch_id, currency), at
-- the legacy reporting grain. Every source_* column is the source system's own
-- declaration from the registered control row — none is an alias of a staged
-- total, because the manifest declares all four controls and the writer
-- publishes them.
--
-- CONSTANT COLUMN: `reject_count` is the literal 0. Modern quarantines a whole
-- batch instead of rejecting rows, so an accepted batch has no rejects by
-- construction. Never assert on it. Every delta column here is genuinely
-- computed.

with control as (
    select * from {{ ref('bronze_merchant_fee_assessment_control') }}
),

staged as (
    select
        batch_id,
        count(*)                                       as staged_count,
        coalesce(sum(gross_amount_brl), 0.00)          as staged_gross_amount,
        coalesce(sum(assessed_fee_brl), 0.00)          as staged_assessed_fee,
        coalesce(sum(calculated_fee_brl), 0.00)        as staged_calculated_fee
    from {{ ref('bronze_merchant_fee_assessment') }}
    group by batch_id
),

applied as (
    select
        batch_id,
        count(*)                                       as applied_count,
        coalesce(sum(gross_amount_brl), 0.00)          as applied_gross_amount,
        coalesce(sum(assessed_fee_brl), 0.00)          as applied_assessed_fee,
        coalesce(sum(calculated_fee_brl), 0.00)        as applied_calculated_fee
    from {{ ref('silver_merchant_fee_assessment') }}
    group by batch_id
)

select
    control.batch_id,
    control.currency,
    control.declared_row_count                                       as source_count,
    staged.staged_count,
    applied.applied_count,
    control.declared_gross_amount                                    as source_gross_amount,
    cast(staged.staged_gross_amount as decimal(14, 2))               as staged_gross_amount,
    cast(applied.applied_gross_amount as decimal(14, 2))             as applied_gross_amount,
    control.declared_assessed_fee                                    as source_assessed_fee,
    cast(staged.staged_assessed_fee as decimal(14, 2))               as staged_assessed_fee,
    cast(applied.applied_assessed_fee as decimal(14, 2))             as applied_assessed_fee,
    control.declared_calculated_fee                                  as source_calculated_fee,
    cast(staged.staged_calculated_fee as decimal(14, 2))             as staged_calculated_fee,
    cast(applied.applied_calculated_fee as decimal(14, 2))           as applied_calculated_fee,
    applied.applied_count - control.declared_row_count               as count_delta,
    cast(
        applied.applied_gross_amount - control.declared_gross_amount
        as decimal(14, 2)
    )                                                                as gross_amount_delta,
    cast(
        applied.applied_assessed_fee - control.declared_assessed_fee
        as decimal(14, 2)
    )                                                                as assessed_fee_delta,
    cast(
        applied.applied_calculated_fee - control.declared_calculated_fee
        as decimal(14, 2)
    )                                                                as calculated_fee_delta,
    cast(
        applied.applied_assessed_fee - applied.applied_calculated_fee
        as decimal(14, 2)
    )                                                                as assessment_calculation_delta,
    0                                                                as reject_count,
    case
        when applied.applied_count = control.declared_row_count
         and applied.applied_gross_amount = control.declared_gross_amount
         and applied.applied_assessed_fee = control.declared_assessed_fee
         and applied.applied_calculated_fee = control.declared_calculated_fee
         and applied.applied_assessed_fee = applied.applied_calculated_fee
        then 'MATCHED'
        else 'MISMATCHED'
    end                                                              as status
from control
join staged  on staged.batch_id  = control.batch_id
join applied on applied.batch_id = control.batch_id
