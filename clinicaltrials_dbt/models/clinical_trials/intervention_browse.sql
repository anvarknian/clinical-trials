{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        derived_section__intervention_browse_module__browse_leaves as browse_leaves,
        derived_section__intervention_browse_module__browse_branches as browse_branches,
        derived_section__intervention_browse_module__meshes as meshes,
        derived_section__intervention_browse_module__ancestors as ancestors
    FROM {{ ref('raw_data') }}
)

select * from source_data