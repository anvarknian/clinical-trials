{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__outcomes_module__primary_outcomes as primary_outcomes,
        protocol_section__outcomes_module__secondary_outcomes as secondary_outcomes,
        protocol_section__outcomes_module__other_outcomes as other_outcomes
    FROM {{ ref('raw_data') }}
)

select * from source_data