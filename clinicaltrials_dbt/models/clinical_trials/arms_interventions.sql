{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__arms_interventions_module__arm_groups as arm_groups,
        protocol_section__arms_interventions_module__interventions as interventions
    FROM {{ ref('raw_data') }}
)

select * from source_data