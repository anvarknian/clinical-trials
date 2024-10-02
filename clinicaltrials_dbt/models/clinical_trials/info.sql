{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        results_section__more_info_module__certain_agreement as certain_agreement,
        results_section__more_info_module__point_of_contact as point_of_contact,
        results_section__more_info_module__limitations_and_caveats as limitations_and_caveats
    FROM {{ ref('raw_data') }}
)

select * from source_data