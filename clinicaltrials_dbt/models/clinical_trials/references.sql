{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__references_module__references as reference,
        protocol_section__references_module__see_also_links as links
    FROM {{ ref('raw_data') }}
)

select * from source_data