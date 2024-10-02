{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        results_section__baseline_characteristics_module__population_description as population_description,
        results_section__baseline_characteristics_module__groups as groups,
        results_section__baseline_characteristics_module__denoms as denoms,
        results_section__baseline_characteristics_module__measures as measures
    FROM {{ ref('raw_data') }}
)

select * from source_data