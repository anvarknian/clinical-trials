{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__ipd_sharing_statement_module__ipd_sharing as ipd_sharing,
        protocol_section__ipd_sharing_statement_module__time_frame as time_frame,
        protocol_section__ipd_sharing_statement_module__access_criteria as access_criteria,
        protocol_section__ipd_sharing_statement_module__url as url,
        protocol_section__ipd_sharing_statement_module__description as description,
        protocol_section__ipd_sharing_statement_module__info_types as info_types
    FROM {{ ref('raw_data') }}
)

select * from source_data