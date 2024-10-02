{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        json_extract_string(protocol_section__identification_module__org_study_id_info, '$.id') as organization_id,
        json_extract_string(protocol_section__identification_module__organization, '$.fullName')  as organization_fullname,
        json_extract_string(protocol_section__identification_module__organization, '$.class')  as organization_class,
        protocol_section__identification_module__brief_title as brief_title,
        protocol_section__identification_module__official_title  as official_title,
        protocol_section__identification_module__acronym as acronym,
        protocol_section__identification_module__secondary_id_infos as secondary_id_infos,
        protocol_section__identification_module__nct_id_aliases as nct_id_aliases,
        has_results as has_results
    FROM {{ ref('raw_data') }}
)

select * from source_data