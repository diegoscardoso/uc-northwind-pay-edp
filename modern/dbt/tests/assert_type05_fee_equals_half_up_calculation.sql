{{ config(tags=['type_05']) }}

-- Every assessed fee must equal its independently calculated HALF_UP fee.
-- The rounding is decided in ingestion; this proves nothing downstream moved it.

select *
from {{ ref('silver_merchant_fee_assessment') }}
where assessment_calculation_delta <> 0.00
