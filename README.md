# clinical-trials

This project allows you to either download CSV/JSON dumps or extract data using pagination from the [ClinicalTrials API](https://clinicaltrials.gov/data-api/api).

For experimental purposes, I chose the second option—data extraction using pagination—as it presents a more challenging and dynamic approach compared to working with a pre-built CSV.

## Technologies Used

- Python
- dbt (Data Build Tool)
- dlt (Data Load Tool)
- DuckDB
- Docker

## Environment Setup

To begin, you'll need an OpenAI API key. Create a `secrets.toml` file to store your credentials securely:

```bash
touch .dlt/secrets.toml
```

Add the following to the file:

```toml
[credentials]
openai_api_key = "<YOUR_OPENAI_API_KEY>"
```

Replace `<YOUR_OPENAI_API_KEY>` with your actual OpenAI API key.

Next, set up a virtual environment for local development:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build the Project

To build the project using Docker, run the following command:

```bash
docker compose up --force-recreate -d
```

## Stopping the Project

To stop the Docker containers, use:

```bash
docker compose stop
```
