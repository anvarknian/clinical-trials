import dlt
import duckdb
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import (
    JSONResponseCursorPaginator
)

from utils.chat import query_chatgpt

API_URL = 'https://clinicaltrials.gov/api/v2'
PIPELINE_NAME = "database"
DESTINATION = "duckdb"

client = RESTClient(
    base_url=API_URL,
    paginator=JSONResponseCursorPaginator(
        cursor_param="pageToken",
        cursor_path="nextPageToken"
    )
)


@dlt.resource(name='clinical_trials',
              write_disposition='replace',
              max_table_nesting=2)
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


@dlt.source(name='standardized_criteria', max_table_nesting=0)
def standardized_criteria_source():
    def criteria_list():
        conn = duckdb.connect(f"{PIPELINE_NAME}.{DESTINATION}")
        query = ("SELECT id, eligibility_criteria "
                 "FROM database.cleaned_data.eligibility")
        titles = conn.sql(query).df()
        yield titles.to_numpy()

    # Using DLT transformer that retrieves a queries in parallel
    @dlt.transformer
    def standardized_criteria(rows):
        # Using defer marks a function to be executed
        # in parallel in a thread pool
        @dlt.defer
        def _get_standardized_criteria(_row):
            inclusion_criteria, exclusion_criteria = query_chatgpt(_row[1])
            return {
                'id': _row[0],
                'inclusion_criteria': inclusion_criteria,
                'exclusion_criteria': exclusion_criteria
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
