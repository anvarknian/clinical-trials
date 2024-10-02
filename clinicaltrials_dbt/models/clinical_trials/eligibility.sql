{{ config(materialized='table') }}

with source_data as (

SELECT
    protocol_section__identification_module__nct_id as id,
    protocol_section__eligibility_module__eligibility_criteria as eligibility_criteria,
    protocol_section__eligibility_module__sex as sex,
    protocol_section__eligibility_module__minimum_age as minimum_age,
    protocol_section__eligibility_module__maximum_age as maximum_age,
    protocol_section__eligibility_module__study_population as study_population,
    protocol_section__eligibility_module__sampling_method as sampling_method,
    protocol_section__eligibility_module__gender_description as gender_description,
    protocol_section__eligibility_module__gender_based as gender_based,
    protocol_section__eligibility_module__healthy_volunteers as healthy_volunteers,
    protocol_section__eligibility_module__std_ages as std_ages
FROM {{ ref('raw_data') }}
)

select * from source_data