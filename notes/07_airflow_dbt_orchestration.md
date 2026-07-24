# Phase 07 – Airflow + dbt Orchestration

## Objective

Integrate **dbt** into the Airflow pipeline so the analytics warehouse is automatically rebuilt and validated after every ETL execution.

Previously, the pipeline stopped after loading raw data into BigQuery.

This phase extends the pipeline by automatically executing:

- dbt run
- dbt test

This eliminates all manual warehouse transformation steps.

---

# Previous Pipeline

```
Kaggle Dataset
        │
        ▼
Weather API
        │
        ▼
Schema Generation
        │
        ▼
Google Cloud Storage
        │
        ▼
BigQuery Raw Dataset
        │
        ▼
Pipeline End
```

Raw tables were available, but analytics models had to be refreshed manually using:

```
dbt run
dbt test
```

---

# New Pipeline

```
Kaggle Dataset
        │
        ▼
Weather API
        │
        ▼
Schema Generation
        │
        ▼
Google Cloud Storage
        │
        ▼
BigQuery Raw Dataset
        │
        ▼
dbt run
        │
        ▼
dbt test
        │
        ▼
Analytics Warehouse Ready
```

Every Airflow execution now produces a fully refreshed warehouse.

---

# Why Integrate dbt into Airflow?

Without orchestration

```
ETL

↓

BigQuery Raw

↓

Developer manually runs

dbt run

↓

Developer manually runs

dbt test
```

Problems

- Manual process
- Easy to forget
- Warehouse becomes outdated
- No automatic validation

---

With Airflow

```
ETL

↓

BigQuery Raw

↓

dbt run

↓

dbt test

↓

Finished
```

Advantages

- Fully automated
- Consistent execution
- Data warehouse always updated
- Automatic data quality validation

---

# Airflow DAG Changes

A new section was added to the DAG.

```
dbt
```

Two tasks were introduced.

```
dbt_run

dbt_test
```

---

# BashOperator

Instead of wrapping dbt inside Python scripts, Airflow executes dbt directly using BashOperator.

Import

```python
from airflow.operators.bash import BashOperator
```

Advantages

- Simpler implementation
- Easier debugging
- Standard Airflow practice
- Native command execution

---

# dbt Run Task

Purpose

Execute every dbt model.

Command

```bash
dbt run
```

Task

```python
task_dbt_run = BashOperator(
    task_id="dbt_run",
    cwd="/opt/airflow/dbt_olist",
    bash_command="dbt run",
)
```

Result

Creates

- Staging Views
- Intermediate Views
- Mart Tables

inside

```
olist_analytics
```

---

# dbt Test Task

Purpose

Validate warehouse quality after transformation.

Command

```bash
dbt test
```

Task

```python
task_dbt_test = BashOperator(
    task_id="dbt_test",
    cwd="/opt/airflow/dbt_olist",
    bash_command="dbt test",
)
```

Executed Tests

- unique
- not_null
- relationships

Result

Warehouse is validated before pipeline completion.

---

# Dependency Changes

Previous DAG

```
load_weather_to_bigquery

↓

End
```

New DAG

```
load_weather_to_bigquery

↓

dbt_run

↓

dbt_test

↓

End
```

Pipeline execution order

```
Start

↓

Download Olist Dataset

↓

Fetch Weather API

↓

Infer Olist Schema

↓

Infer Weather Schema

↓

Upload Olist to GCS

↓

Upload Weather to GCS

↓

Create BigQuery Dataset

↓

Create BigQuery Tables

↓

Load Olist Raw Tables

↓

Load Weather Table

↓

dbt run

↓

dbt test

↓

End
```

---

# Docker Considerations

The Airflow Docker image already included

```
dbt-core

dbt-bigquery
```

from

```
requirements.txt
```

No additional packages were required.

---

# profiles.yml

The project migrated from DuckDB to BigQuery.

Old profile

```yaml
type: duckdb
```

New profile

```yaml
type: bigquery
```

Credential

```yaml
keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS', '../config/service-account.json') }}"
```

Benefits

- Works locally
- Works inside Docker
- Works on Compute Engine VM
- Single configuration file

---

# Deployment

Changes were committed to GitHub.

```
git add .

git commit

git push
```

VM updated using

```
git pull origin main
```

Docker rebuilt

```
docker compose down

docker compose build --no-cache

docker compose up -d
```

This ensured

- Latest DAG
- Latest dbt profile
- Latest project files

were available inside Airflow containers.

---

# Issue Encountered

Problem

The VM still contained the old DuckDB profile.

```
type: duckdb
```

Reason

Git pull failed because Airflow-generated log files were tracked by Git and owned by Docker user UID 50000.

Symptoms

```
git pull

↓

Merge blocked

↓

profiles.yml not updated

↓

dbt debug failed
```

Resolution

Changed ownership

```bash
sudo chown -R $USER:$USER logs
```

Performed

```
git pull origin main
```

Verified

```
profiles.yml

↓

type: bigquery
```

Docker rebuilt successfully afterwards.

---

# Validation

Verified inside container

```
dbt --version
```

Result

```
dbt 1.12

dbt-bigquery installed
```

Verified project mount

```
/opt/airflow/dbt_olist
```

contained

```
dbt_project.yml

profiles.yml

models
```

Airflow successfully executed

```
dbt_run

↓

dbt_test
```

---

# Final Airflow Execution

Successful execution order

```
download_olist_dataset

↓

fetch_weather_api

↓

infer_olist_schema

↓

infer_weather_schema

↓

upload_olist_to_gcs

↓

upload_weather_to_gcs

↓

create_bigquery_datasets

↓

create_bigquery_tables

↓

load_olist_to_bigquery

↓

load_weather_to_bigquery

↓

dbt_run

↓

dbt_test

↓

End
```

Every task completed successfully.

No failures occurred.

---

# What dbt Run Does

```
Raw Dataset

↓

Staging Views

↓

Intermediate Views

↓

Mart Tables
```

Warehouse becomes available for reporting.

---

# What dbt Test Does

Runs automated warehouse validation.

Current tests

```
unique

not_null

relationships
```

Purpose

- Validate primary keys
- Validate mandatory fields
- Validate foreign key relationships

Current project

```
32 Tests

PASS = 32

FAIL = 0
```

---

# Final Architecture

```
                Airflow

                    │

                    ▼

        Download Olist Dataset

                    │

                    ▼

          Fetch Weather API

                    │

                    ▼

      Generate BigQuery Schemas

                    │

                    ▼

     Upload Files to Cloud Storage

                    │

                    ▼

       Load BigQuery Raw Dataset

                    │

                    ▼

                dbt run

                    │

                    ▼

                dbt test

                    │

                    ▼

      BigQuery Analytics Warehouse

                    │

                    ▼

          Ready for Power BI
```

---

# Files Modified

```
dags/olist_pipeline.py

dbt_olist/profiles.yml

requirements.txt
```

---

# Deliverables

Completed

- Airflow orchestrates dbt automatically
- Analytics warehouse refresh automated
- Warehouse validation automated
- No manual dbt execution required
- End-to-end ELT pipeline completed

---

# Key Lessons Learned

- Airflow can orchestrate both ETL and ELT workflows.
- dbt should execute immediately after raw data is loaded.
- BashOperator is a simple and effective way to integrate dbt.
- `dbt run` rebuilds warehouse models.
- `dbt test` validates warehouse quality.
- Keeping `profiles.yml` environment-agnostic allows the same project to run locally and on a VM.
- Container file ownership can affect Git operations when runtime-generated files are tracked.

---

# Next Phase

## Phase 08 – Power BI Dashboard

Goal

```
BigQuery Analytics Warehouse

↓

Power BI

↓

Executive Dashboard

↓

Business KPIs

↓

Interactive Visualizations
```