{{ config(materialized='table') }}

with source_data as (
    SELECT
        protocol_section__identification_module__nct_id as id,
        results_section__adverse_events_module__frequency_threshold as frequency_threshold,
        results_section__adverse_events_module__time_frame as time_frame,
        results_section__adverse_events_module__description as adverse_events_description,
        results_section__adverse_events_module__event_groups as event_groups ,
        results_section__adverse_events_module__serious_events as serious_events ,
        results_section__adverse_events_module__other_events as other_events
    FROM {{ ref('raw_data') }}
)

select * from source_data