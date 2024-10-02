{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        annotation_section__annotation_module__unposted_annotation as unposted_annotation
    FROM {{ ref('raw_data') }}
)

select * from source_data