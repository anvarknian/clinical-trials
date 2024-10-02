{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        results_section__participant_flow_module__groups as groups,
        results_section__participant_flow_module__periods as periods,
        results_section__participant_flow_module__pre_assignment_details as pre_assignment_details,
        results_section__participant_flow_module__recruitment_details as recruitment_details
    FROM {{ ref('raw_data') }}
)

select * from source_data