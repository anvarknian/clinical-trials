{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__status_module__status_verified_date as status_verified_date,
        protocol_section__status_module__overall_status as overall_status,
        protocol_section__status_module__study_first_submit_date as study_submit_date,
        protocol_section__status_module__study_first_submit_qc_date as study_submit_qc_date,
        protocol_section__status_module__results_first_submit_date as results_first_submit_date,
        protocol_section__status_module__results_first_submit_qc_date as results_first_submit_qc_date,
        protocol_section__status_module__last_update_submit_date as last_update_submit_date,
        protocol_section__status_module__disp_first_submit_date as disp_first_submit_date,
        protocol_section__status_module__disp_first_submit_qc_date as disp_first_submit_qc_date,
        protocol_section__status_module__expanded_access_info as expanded_access_info,
        protocol_section__status_module__start_date_struct as start_date_struct,
        protocol_section__status_module__primary_completion_date_struct as primary_completion_date_struct,
        protocol_section__status_module__completion_date_struct as completion_date_struct,
        protocol_section__status_module__study_first_post_date_struct as study_first_post_date_struct,
        protocol_section__status_module__results_first_post_date_struct as results_first_post_date_struct,
        protocol_section__status_module__last_update_post_date_struct as last_update_post_date_struct,
        protocol_section__status_module__disp_first_post_date_struct as disp_first_post_date_struct
    FROM {{ ref('raw_data') }}
)

select * from source_data