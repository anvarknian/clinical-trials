{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__design_module__study_type as study_type,
        protocol_section__design_module__target_duration as target_duration,
        protocol_section__design_module__patient_registry as patient_registry,
        protocol_section__design_module__phases as phases,
        protocol_section__design_module__design_info as design_info,
        protocol_section__design_module__enrollment_info as enrollment_info,
        protocol_section__design_module__bio_spec as bio_spec
    FROM {{ ref('raw_data') }}
)

select * from source_data