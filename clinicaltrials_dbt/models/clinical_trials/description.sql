{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__description_module__brief_summary as brief_summary,
        protocol_section__description_module__detailed_description as detailed_description
    FROM {{ ref('raw_data') }}
)

select * from source_data