{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        results_section__outcome_measures_module__outcome_measures as outcome_measures
    FROM {{ ref('raw_data') }}
)

select * from source_data