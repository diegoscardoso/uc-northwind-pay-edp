{{ config(tags=['type_05']) }}

-- All four Type 05 source controls are real declarations from the source
-- manifest, registered beside the data. Nothing here is an alias of a staged
-- total; a declaration that disagreed with the rows never reached landing.

select
    batch_id,
    type_number,
    contract_code,
    currency,
    cast(declared_detail_count as integer)           as declared_row_count,
    cast(computed_detail_count as integer)           as computed_row_count,
    cast(declared_gross_amount as decimal(14, 2))    as declared_gross_amount,
    cast(computed_gross_amount as decimal(14, 2))    as computed_gross_amount,
    cast(declared_assessed_fee as decimal(14, 2))    as declared_assessed_fee,
    cast(computed_assessed_fee as decimal(14, 2))    as computed_assessed_fee,
    cast(declared_calculated_fee as decimal(14, 2))  as declared_calculated_fee,
    cast(computed_calculated_fee as decimal(14, 2))  as computed_calculated_fee,
    cast(record_count as integer)                    as record_count,
    raw_sha256,
    parquet_sha256,
    source_file
from {{ source('landing', 'merchant_fee_assessment_control') }}
