# Phase 02 – Google Compute Engine & Apache Airflow

## Objective

The objective of this phase is to provision a Google Compute Engine virtual machine, deploy Apache Airflow using Docker Compose, and verify that the orchestration platform is accessible through the public internet.

This Airflow instance will orchestrate the complete cloud data engineering pipeline in later phases.

---

# Architecture

MacBook

↓

GitHub Repository

↓

Google Compute Engine VM

↓

Docker + Docker Compose

↓

Apache Airflow

↓

Future ETL Pipeline

---

# Virtual Machine

Cloud Platform

Google Cloud Platform

Service

Compute Engine

Operating System

Ubuntu LTS

Purpose

Host the Apache Airflow environment.

---

# Connect to VM

Using Google Cloud CLI

```bash
gcloud compute ssh olist-airflow-vm --zone asia-southeast1-b
```

---

# Clone Repository

```bash
git clone https://github.com/KHakim96/olist-gcp-data-engineering-pipeline.git

cd olist-gcp-data-engineering-pipeline
```

---

# Docker Installation

Update packages

```bash
sudo apt update
sudo apt upgrade -y
```

Install Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Add current user to Docker group

```bash
sudo usermod -aG docker $USER
```

Reconnect to VM

Verify installation

```bash
docker --version

docker compose version
```

---

# Repository Structure

The project contains:

```
Dockerfile
docker-compose.yml
config/
dags/
scripts/
dbt_olist/
```

---

# Environment Variables

Create

```
.env
```

Configuration

```text
POSTGRES_DB=airflow
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow

AIRFLOW_UID=50000

AIRFLOW__CORE__LOAD_EXAMPLES=False

AIRFLOW__CORE__FERNET_KEY=

AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True

AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

GOOGLE_CLOUD_PROJECT=olist-gcp-data-engineering

GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/config/service-account.json

GCS_BUCKET=olist-gcp-data-lake-luqman

BQ_RAW_DATASET=olist_raw

BQ_ANALYTICS_DATASET=olist_analytics
```

---

# Required Directories

Create

```bash
mkdir logs
mkdir plugins
```

Permissions

```bash
chmod -R 777 logs
chmod -R 777 plugins
```

---

# Build Airflow Image

```bash
docker compose build --no-cache
```

---

# Initialise Airflow

```bash
docker compose up airflow-init
```

Expected output

```
Database migrating done
```

Create administrator

```bash
docker compose exec airflow-webserver airflow users create \
--username admin \
--password admin \
--firstname Luqman \
--lastname Hakim \
--role Admin \
--email admin@example.com
```

---

# Start Services

```bash
docker compose up -d
```

Verify

```bash
docker compose ps
```

Expected

```
airflow_postgres

airflow_scheduler

airflow_webserver
```

---

# Verify Containers

```bash
docker ps
```

---

# Verify Airflow Health

```bash
curl http://localhost:8080/health
```

Expected

```json
{
 "scheduler":{
  "status":"healthy"
 }
}
```

---

# Public Access

VM External IP

```
34.126.186.95
```

Browser

```
http://34.126.186.95:8080
```

---

# Firewall

Create VPC Firewall Rule

Allow

```
TCP

8080
```

Source

```
0.0.0.0/0
```

Without this rule the browser returns

```
ERR_CONNECTION_TIMED_OUT
```

---

# Issues Encountered

## Airflow Permission Denied

Error

```
Permission denied

airflow.cfg
```

Cause

Mounted project directory ownership.

Solution

Removed user override.

Allowed Airflow container to manage its own configuration.

---

## Logs Permission

Error

```
Permission denied

/opt/airflow/logs
```

Solution

Created

```
logs/
plugins/
```

Updated permissions

```bash
chmod -R 777 logs
chmod -R 777 plugins
```

---

## Gunicorn Timeout

Error

```
No response from gunicorn master
```

Solution

Reduced workers

```
airflow webserver --workers 1
```

---

## Environment Variables Missing

Error

```
Could not parse SQLAlchemy URL
```

Cause

Missing

```
.env
```

Solution

Copied correct .env file to VM.

---

## Firewall Timeout

Browser

```
ERR_CONNECTION_TIMED_OUT
```

Cause

VPC Firewall missing.

Solution

Create firewall rule allowing TCP 8080.

---

## Admin Login Error

Issue

Airflow UI displayed

```
Oops!

Something bad has happened
```

Cause

Corrupted administrator account.

Solution

Delete and recreate administrator.

```bash
docker compose exec airflow-webserver airflow users delete --username admin

docker compose exec airflow-webserver airflow users create ...
```

---

# Validation Checklist

- Compute Engine running

- Docker installed

- Docker Compose installed

- PostgreSQL running

- Airflow Scheduler running

- Airflow Webserver running

- Airflow Metadata Database initialised

- Administrator account created

- Public UI accessible

- Firewall configured

- Repository deployed

---

# Deliverables

Completed

- Compute Engine VM

- Docker environment

- Apache Airflow

- PostgreSQL metadata database

- Administrator account

- Public Airflow UI

- GitHub deployment workflow

---

# Status

Completed