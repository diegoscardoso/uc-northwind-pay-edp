{{ config(tags=['type_05']) }}

-- Silver: conformed assessment at the Bronze grain. Money columns keep their
-- Bronze names so conservation can compare them without renaming.

select
    batch_id,
    source_record_number,
    assessment_id,
    merchant_id,
    merchant_tax_id_masked,
    fee_code,
    description,
    gross_amount_brl,
    rate_percent,
    assessed_fee_brl,
    calculated_fee_brl,
    cast(assessment_date as date)   as assessment_date,
    assessment_date                 as assessment_date_text,
    rounding_mode,
    source_file
from {{ ref('bronze_merchant_fee_assessment') }}
