{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        document_section__large_document_module__large_docs as large_docs
    FROM {{ ref('raw_data') }}
)

select * from source_data