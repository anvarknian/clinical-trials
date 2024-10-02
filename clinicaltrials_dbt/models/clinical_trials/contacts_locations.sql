{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__contacts_locations_module__overall_officials as overall_officials,
        protocol_section__contacts_locations_module__locations as locations
    FROM {{ ref('raw_data') }}
)

select * from source_data