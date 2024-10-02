{{ config(materialized='table') }}

with source_data as (

    SELECT
        protocol_section__identification_module__nct_id as id,
        protocol_section__sponsor_collaborators_module__responsible_party as responsible_party,
        protocol_section__sponsor_collaborators_module__lead_sponsor as lead_sponsor,
        protocol_section__sponsor_collaborators_module__collaborators as collaborators
    FROM {{ ref('raw_data') }}
)

select * from source_data