{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__oversight_module__is_fda_regulated_drug as is_fda_regulated_drug,
        protocol_section__oversight_module__is_fda_regulated_device as is_fda_regulated_device,
        protocol_section__oversight_module__oversight_has_dmc as oversight_has_dmc,
        protocol_section__oversight_module__is_us_export as is_us_export
    FROM {{ ref('raw_data') }}
)

select * from source_data