{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__conditions_module__keywords as keywords,
        protocol_section__conditions_module__conditions as conditions
    FROM {{ ref('raw_data') }}
)

select * from source_data