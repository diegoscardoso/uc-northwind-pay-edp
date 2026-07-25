{{ config(tags=['type_05']) }}

-- HALF_UP, proven in SQL without trusting any round() implementation.
-- fee_cents = gross x rate is exact at scale five. calculated_fee_brl is the
-- HALF_UP result exactly when its cents value n satisfies
-- n - 0.5 <= fee_cents < n + 0.5, with the tie at n - 0.5 rounding upward —
-- so equality is allowed on the lower bound and forbidden on the upper.
-- A row also fails if the source's assessed fee disagrees with the
-- recomputation, which the ingestion gate should have made impossible.

with recomputed as (
    select
        batch_id,
        source_record_number,
        assessed_fee_brl,
        calculated_fee_brl,
        cast(gross_amount_brl as decimal(28, 2)) * rate_percent  as fee_cents,
        cast(calculated_fee_brl as decimal(28, 2)) * 100         as calculated_cents
    from {{ ref('bronze_merchant_fee_assessment') }}
)

select batch_id, source_record_number
from recomputed
where assessed_fee_brl <> calculated_fee_brl
   or fee_cents < calculated_cents - 0.5
   or fee_cents >= calculated_cents + 0.5
