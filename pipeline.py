import json

import dlt
import duckdb
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import JSONResponseCursorPaginator

from utils.chat import standardize_disease_name

API_URL = 'https://clinicaltrials.gov/api/v2'
PIPELINE_NAME = "database"
DESTINATION = "duckdb"
MODE = 'replace'

client = RESTClient(
    base_url=API_URL,
    paginator=JSONResponseCursorPaginator(cursor_param="pageToken", cursor_path="nextPageToken")
)


@dlt.resource(name='clinical_trials', write_disposition=MODE, max_table_nesting=2)
def clinical_trials_resource():
    for page in client.paginate("/studies?filter.overallStatus=COMPLETED"):
        studies = page.response.json().get('studies', [])
        yield studies


@dlt.source(name="clinical_trials")
def clinical_trials_source():
    return clinical_trials_resource()


def load_clinical_trials():
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME, destination=DESTINATION,
        dataset_name="raw_data", progress="log"
    )

    # limit number of yield for dev purpose
    load_info = pipeline.run(clinical_trials_source().add_limit(10))
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


def run_dbt_package():
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME, destination=DESTINATION,
        dataset_name='cleaned_data', progress="log"
    )

    venv = dlt.dbt.get_venv(pipeline)

    dbt = dlt.dbt.package(
        pipeline,
        "clinicaltrials_dbt",
        venv=venv
    )

    models = dbt.run_all()
    for m in models:
        print(
            f"Model {m.model_name} materialized" +
            f" in {m.time}" +
            f" with status {m.status}" +
            f" and message {m.message}")


#
# @dlt.resource(name='standardized_diagnosis', write_disposition=MODE)
# def openai_pipeline(df):
#     for index, row in df.iterrows():
#         result = standardize_disease_name(row['brief_title'])
#         yield {'id': row['id'], 'description': row['brief_title'], 'diagnosis': result}
#
# def run_openai_pipeline(prompts_list):
#     pipeline = dlt.pipeline(
#         pipeline_name=DATABASE_NAME, destination=DEFAULT_DESTINATION,
#         dataset_name="cleaned_data", progress="log"
#     )
#     info = pipeline.run(openai_pipeline(prompts_list))
#     print(info)
#     print(pipeline.last_trace.last_normalize_info)
#
# def read_cleaned_data():
#     conn = duckdb.connect(f"{DATABASE_NAME}.{DEFAULT_DESTINATION}")
#     titles = conn.sql("SELECT id, brief_title FROM database.cleaned_data.clinical_trials").df()
#     return titles


@dlt.source(name='standardized_criteria',max_table_nesting=0)
def standardized_criteria_source():
    # @dlt.resource(write_disposition="replace", selected=False)
    def criteria_list():
        conn = duckdb.connect(f"{PIPELINE_NAME}.{DESTINATION}")
        titles = conn.sql("SELECT id, eligibility_criteria FROM database.cleaned_data.eligibility").df()
        yield titles.to_numpy()

    @dlt.transformer
    def standardized_criteria(rows):
        @dlt.defer
        def _get_standardized_criteria(_row):
            result = json.loads(standardize_disease_name(_row[1]))
            return {
                'id': _row[0],
                'inclusion_criteria': result.get('inclusion_criteria',[]),
                'exclusion_criteria': result.get('exclusion_criteria',[])
            }

        for row in rows:
            yield _get_standardized_criteria(row)

    return (criteria_list | standardized_criteria)


def run_openai_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME, destination=DESTINATION,
        dataset_name="cleaned_data", progress="log"
    )
    info = pipeline.run(standardized_criteria_source())
    print(info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_clinical_trials()
    run_dbt_package()
    run_openai_pipeline()
