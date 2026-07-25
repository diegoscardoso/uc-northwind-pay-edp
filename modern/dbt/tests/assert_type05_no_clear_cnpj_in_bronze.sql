{{ config(tags=['type_05']) }}

-- Privacy: the masked CNPJ must match its contract shape exactly, and no
-- description may carry a digit run long enough to be a raw document — the
-- contract forbids runs of eleven or more, which covers every CNPJ.

select batch_id, source_record_number
from {{ ref('bronze_merchant_fee_assessment') }}
where not regexp_matches(merchant_tax_id_masked, '^\*{10}[0-9]{4}$')
   or regexp_matches(description, '[0-9]{11}')
