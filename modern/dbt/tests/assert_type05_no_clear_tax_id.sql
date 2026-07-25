{{ config(tags=['type_05']) }}

-- Privacy: no Bronze row may carry a clear fourteen-digit CNPJ. Structural
-- rather than value-based, so it holds for data it has never seen.

select *
from {{ ref('bronze_merchant_fee_assessment') }}
where not regexp_matches(merchant_tax_id_masked, '^\*{10}[0-9]{4}$')
   or regexp_matches(merchant_tax_id_masked, '[0-9]{14}')
