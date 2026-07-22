# Phase 05 – Airflow Orchestration

## Objective

Build an end-to-end workflow using Apache Airflow to orchestrate the complete GCP data engineering pipeline.

The DAG automates:

Kaggle Dataset
        ↓
Weather API
        ↓
Schema Inference
        ↓
Google Cloud Storage
        ↓
BigQuery Raw Layer

---

# Final Status

Status:
✅ Completed

Airflow Version:
2.11.0

Executor:
LocalExecutor

Deployment:
Docker Compose

Environment:
- Local Mac (Development)
- Google Compute Engine VM (Deployment)

---

# Project Structure

dags/
    olist_pipeline.py

scripts/
    sources/
        kaggle/
        weather/

    schemas/

    gcs/

    bigquery/

config/
    service-account.json

docker-compose.yml

Dockerfile

requirements.txt

---

# Docker Image

Dockerfile

FROM apache/airflow:2.11.0-python3.11

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

Purpose

Creates a custom Airflow image containing:

- Google Cloud SDK libraries
- BigQuery libraries
- Storage libraries
- Python project dependencies

---

# Airflow Services

The project uses the official Airflow Docker Compose architecture.

Services

1. PostgreSQL

Purpose

Stores Airflow metadata.

Contains

- DAG metadata
- Task history
- Scheduler information
- Users

Image

postgres:16

---

2. Airflow Init

Purpose

Runs once during startup.

Responsibilities

- Initialize database
- Run migrations
- Create admin account

Runs only once.

---

3. Scheduler

Purpose

Responsible for

- Parsing DAGs
- Scheduling tasks
- Triggering execution
- Updating task states

Command

scheduler

---

4. Webserver

Purpose

Provides Airflow UI.

Command

webserver

Port

8080

---

# Executor

Executor

LocalExecutor

Reason

Allows parallel task execution on a single machine.

Suitable for

- Local development
- Portfolio projects
- Small production workloads

---

# DAG

DAG ID

olist_gcp_data_engineering_pipeline

Description

End-to-End Olist GCP Data Engineering Pipeline

Schedule

None

Pipeline is manually triggered.

Catchup

False

Retries

2

Owner

Luqman

---

# DAG Tasks

1

start

↓

2

download_olist_dataset

Downloads latest Olist dataset.

↓

3

fetch_weather_api

Downloads latest weather data.

↓

4

infer_olist_schema

Generates BigQuery schema automatically.

↓

5

infer_weather_schema

Generates weather schema.

↓

6

upload_olist_to_gcs

Uploads parquet/data to GCS.

↓

7

upload_weather_to_gcs

Uploads weather file.

↓

8

create_bigquery_datasets

Creates

- olist_raw
- olist_analytics

↓

9

create_bigquery_tables

Creates raw BigQuery tables.

↓

10

load_olist_to_bigquery

Loads Olist dataset.

↓

11

load_weather_to_bigquery

Loads weather dataset.

↓

12

end

---

# Airflow UI

Verified

✓ DAG discovered

✓ DAG parsed

✓ DAG manually triggered

✓ Graph View

✓ Grid View

✓ Task Logs

✓ Success Status

---

# Local Development

Platform

MacBook Air M2

Docker Desktop

Result

All services healthy.

Containers

Postgres

Airflow Scheduler

Airflow Webserver

Airflow Init

Pipeline executes successfully.

---

# Google Cloud VM Deployment

Platform

Google Compute Engine

Deployment

Docker Compose

SSH

gcloud compute ssh ...

---

# Major Issue Encountered

Issue

Airflow UI inaccessible.

Symptoms

Connection refused

Connection reset by peer

Gunicorn timeout

Webserver continuously restarting.

Initially suspected

- Docker
- Firewall
- Gunicorn
- Compose
- Airflow configuration

None were root cause.

---

# Root Cause

VM memory insufficient.

Machine

2 GB RAM

Kernel logs

Out of memory

Killed process

gunicorn master

The Linux OOM Killer terminated the Airflow webserver before it finished startup.

This caused

curl localhost:8080

to fail repeatedly.

---

# Evidence

journalctl

Out of memory

Killed process gunicorn

docker stats

Airflow Scheduler

≈570 MB

Airflow Webserver

≈636 MB

Postgres

≈50 MB

Total

≈1.25 GB

Operating system + Docker exceeded available 2 GB RAM.

---

# Resolution

Upgraded VM to a larger machine type.

Result

Airflow UI loads successfully.

Scheduler healthy.

Webserver healthy.

Pipeline executes normally.

---

# Lessons Learned

1.

Official Airflow Docker Compose is more stable than a custom minimal Compose.

2.

Airflow requires more RAM than expected.

2 GB is insufficient for

- Scheduler
- Webserver
- PostgreSQL

3.

Always inspect kernel OOM logs before debugging Airflow configuration.

Useful commands

free -h

docker stats

sudo journalctl -k | grep -i oom

4.

Use the official Airflow image whenever possible.

Avoid custom startup scripts.

---

# Verification Checklist

Docker Image builds

PASS

Docker Compose starts

PASS

Scheduler healthy

PASS

Webserver healthy

PASS

Postgres healthy

PASS

Airflow UI

PASS

DAG parsed

PASS

Manual trigger

PASS

Task execution

PASS

GCS upload

PASS

BigQuery datasets

PASS

BigQuery tables

PASS

BigQuery load

PASS

End-to-end pipeline

PASS

---

# Final Deliverables

✓ Dockerfile

✓ Official docker-compose.yml

✓ Airflow DAG

✓ Python ETL scripts

✓ Google Cloud Storage integration

✓ BigQuery integration

✓ End-to-end orchestration

✓ Deployment on Google Compute Engine

---

# Phase Outcome

Successfully implemented an end-to-end Apache Airflow orchestration layer for the Olist GCP Data Engineering Pipeline.

The pipeline is fully containerized, reproducible, and deployable on both local development and Google Compute Engine.