{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        derived_section__misc_info_module__version_holder as version_holder,
        derived_section__misc_info_module__submission_tracking as submission_tracking,
        derived_section__misc_info_module__removed_countries as removed_countries
    FROM {{ ref('raw_data') }}
)

select * from source_data