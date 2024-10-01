# clinical-trials

For this project, you can either download CSV/JSON dumps OR extract data using Pagination from [ClinicalTrials](https://clinicaltrials.gov/data-api/api).

For Experimental purpose, I used the second option (Using Pagination) because it seemed more challenging rather than dealing with a ready CSV.


## Tech used:

- python
- dbt
- dlt
- duckdb
- docker


## Env Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Build Command
```bash
docker compose up --force-recreate -d
```

## Stop Command 
```bash
docker compose stop
```