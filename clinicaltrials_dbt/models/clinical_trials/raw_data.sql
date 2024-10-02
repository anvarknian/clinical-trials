{{ config(materialized='view') }}

with source_data as (
    SELECT
        *
    FROM raw_data.clinical_trials
)

select * from source_data



