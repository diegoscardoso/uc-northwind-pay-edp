{{ config(tags=['type_05']) }}

-- Bronze: typed and source-aligned. Grain: (batch_id, source_record_number).

select
    batch_id,
    source_file,
    cast(source_record_number as integer)       as source_record_number,
    assessment_id,
    merchant_id,
    merchant_tax_id_masked,
    fee_code,
    description,
    cast(gross_amount_brl as decimal(14, 2))    as gross_amount_brl,
    cast(rate_percent as decimal(6, 3))         as rate_percent,
    cast(assessed_fee_brl as decimal(14, 2))    as assessed_fee_brl,
    cast(calculated_fee_brl as decimal(14, 2))  as calculated_fee_brl,
    assessment_date,
    rounding_mode
from {{ source('landing', 'merchant_fee_assessment') }}
