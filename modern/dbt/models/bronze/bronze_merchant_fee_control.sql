{{ config(tags=['type_05']) }}

-- The dlt control extractor is generic across types and registers
-- `detail_count` and `net_amount`. Type 05 counts assessment rows and governs
-- the assessed fee, so those are the two that travelled; Bronze gives them back
-- their domain names here rather than leaking the transport vocabulary upward.

select
    batch_id,
    type_number,
    contract_code,
    currency,
    cast(declared_detail_count as integer)          as declared_row_count,
    cast(computed_detail_count as integer)          as computed_row_count,
    cast(declared_net_amount as decimal(18, 2))     as declared_assessed_fee,
    cast(computed_net_amount as decimal(18, 2))     as computed_assessed_fee,
    cast(record_count as integer)                   as record_count,
    raw_sha256,
    parquet_sha256,
    source_file
from {{ source('landing', 'merchant_fee_assessment_control') }}
