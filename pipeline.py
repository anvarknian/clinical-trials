import logging

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import JSONResponseCursorPaginator

logger = logging.getLogger(__name__)
FILE_URL = 'https://clinicaltrials.gov/api/v2'

client = RESTClient(
    base_url=FILE_URL,
    paginator=JSONResponseCursorPaginator(cursor_param="pageToken", cursor_path="nextPageToken")
)


@dlt.resource(write_disposition='replace')
def get_data():
    for page in client.paginate("/studies"):
        yield page


def load_clinical_trials() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="clinical_trials",
        destination='duckdb',
        dataset_name="raw_data",
    )

    # limit number of yield for dev purpose
    load_info = pipeline.run(get_data().add_limit(10))
    logger.info(load_info)

if __name__ == "__main__":
    load_clinical_trials()
