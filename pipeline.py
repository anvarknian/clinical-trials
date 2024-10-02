import logging

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import JSONResponseCursorPaginator

API_URL = 'https://clinicaltrials.gov/api/v2'

client = RESTClient(
    base_url=API_URL,
    paginator=JSONResponseCursorPaginator(cursor_param="pageToken", cursor_path="nextPageToken")
)


@dlt.resource(name='clinical_trials', write_disposition='replace', max_table_nesting=2)
def clinical_trials_resource():
    for page in client.paginate("/studies?filter.overallStatus=COMPLETED"):
        studies = page.response.json().get('studies', [])
        yield studies


@dlt.source(name="clinical_trials")
def clinical_trials_source():
    return clinical_trials_resource()


def load_clinical_trials():
    pipeline = dlt.pipeline(
        pipeline_name="database",
        destination='duckdb',
        dataset_name="raw_data",
        progress="log"
    )

    # limit number of yield for dev purpose
    load_info = pipeline.run(clinical_trials_source().add_limit(10))
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


def run_dbt_package():
    pipeline = dlt.pipeline(
        pipeline_name='database',
        destination='duckdb',
        dataset_name='cleaned_data',
        progress="log"
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


if __name__ == "__main__":
    load_clinical_trials()
    run_dbt_package()