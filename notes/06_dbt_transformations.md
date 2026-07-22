# Phase 06 – dbt Transformations (BigQuery Data Warehouse)

## Objective

Build a modern analytics warehouse using **dbt** on top of the raw data stored in **BigQuery**.

This phase transforms raw operational data into clean, analytics-ready dimension and fact tables for reporting and business intelligence.

---

# Architecture

```text
Kaggle CSV + Weather API
            │
            ▼
      Python ETL
            │
            ▼
 Google Cloud Storage
      (Data Lake)
            │
            ▼
BigQuery Raw Dataset
   (olist_raw)
            │
            ▼
          dbt
            │
     ┌──────┴──────┐
     ▼             ▼
 Staging        Intermediate
   Views            Views
          │
          ▼
        Mart
       Tables
          │
          ▼
 BigQuery Analytics
 (olist_analytics)
```

---

# Why dbt?

The raw dataset should never be used directly by dashboards.

Instead, dbt creates a proper warehouse layer by:

- Cleaning raw data
- Standardizing schemas
- Applying business logic
- Creating reusable models
- Testing data quality
- Version controlling SQL transformations

---

# dbt Project Structure

```
dbt_olist/

├── dbt_project.yml
├── profiles.yml
├── macros/
├── tests/
└── models/
    ├── staging/
    ├── intermediate/
    └── marts/
```

---

# BigQuery Datasets

Raw dataset

```
olist_raw
```

Contains

- Raw CSV imports
- Weather data
- No transformations

Analytics dataset

```
olist_analytics
```

Contains

- Staging Views
- Intermediate Views
- Dimension Tables
- Fact Tables
- Dashboard Models

---

# dbt Configuration

## dbt_project.yml

Project

```yaml
name: olist
```

Profile

```yaml
profile: olist
```

Materialization

```yaml
staging:
    +materialized: view

intermediate:
    +materialized: view

marts:
    +materialized: table
```

Meaning

```
Raw

↓

View

↓

View

↓

Table
```

---

# profiles.yml

Migrated from DuckDB to BigQuery.

Old

```yaml
type: duckdb
```

New

```yaml
type: bigquery
```

Authentication

```yaml
method: service-account
```

Project

```yaml
project: olist-gcp-data-engineering
```

Dataset

```yaml
dataset: olist_analytics
```

Location

```yaml
asia-southeast1
```

Credential

```yaml
keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS', '../config/service-account.json') }}"
```

This allows the same configuration to work on:

- Mac
- Docker
- GCP VM

without modifying the file.

---

# Source Mapping

Raw BigQuery tables use Kaggle names.

Example

```
olist_orders_dataset
```

instead of

```
orders
```

Instead of renaming BigQuery tables, dbt uses **identifier mapping**.

Example

```yaml
- name: orders
  identifier: olist_orders_dataset
```

Result

SQL remains clean.

```sql
{{ source('raw','orders') }}
```

dbt automatically maps it to

```
olist_orders_dataset
```

---

# Warehouse Layers

## 1. Staging Layer

Materialization

```
View
```

Purpose

- Standardize raw data
- Rename columns
- Data type conversion
- Basic cleaning

Models

```
stg_customers

stg_orders

stg_products

stg_sellers

stg_geolocation

stg_order_items

stg_order_payments

stg_order_reviews

stg_category_translation
```

Characteristics

- Reads directly from raw tables
- No joins
- No aggregations
- Lightweight transformations only

---

## 2. Intermediate Layer

Materialization

```
View
```

Purpose

Apply reusable business logic.

Models

```
int_orders

int_customer_orders

int_delivery_metrics

int_payment_summary

int_product_sales

int_review_metrics

int_order_items
```

Examples

- Delivery days
- Shipping days
- Delay days
- Payment summaries
- Customer order metrics

Characteristics

- Joins between staging models
- Derived business metrics
- Still virtual (no physical storage)

---

## 3. Mart Layer

Materialization

```
Table
```

Purpose

Create analytics-ready warehouse tables optimized for BI tools.

Dimension Tables

```
dim_customer

dim_product

dim_seller

dim_geolocation

dim_date
```

Fact Tables

```
fact_orders

fact_order_items

fact_payments

fact_reviews
```

Dashboard Table

```
executive_dashboard
```

Characteristics

- Physically stored in BigQuery
- Faster dashboard queries
- Reduced computation cost
- Final reporting layer

---

# Why Views?

Staging and Intermediate models are Views because they:

- Consume no additional storage
- Always reflect latest raw data
- Are inexpensive to maintain
- Simplify development

Flow

```
Raw

↓

View

↓

View
```

---

# Why Tables?

Mart models are Tables because dashboards constantly query them.

Advantages

- Faster performance
- Lower query cost
- Better BI experience
- Reduced repeated computation

Flow

```
Views

↓

Fact Table

↓

Power BI
```

---

# DuckDB → BigQuery Migration

Most SQL models were reused.

Required changes

## profiles.yml

Changed adapter

```
duckdb

↓

bigquery
```

---

## sources.yml

Mapped logical source names using

```yaml
identifier:
```

instead of renaming BigQuery tables.

---

## SQL Compatibility

Changed

DuckDB

```sql
DATE_DIFF('day', start, end)
```

BigQuery

```sql
DATE_DIFF(
    DATE(end),
    DATE(start),
    DAY
)
```

---

Changed

DuckDB

```sql
CAST(timestamp AS DATE)
```

BigQuery

```sql
DATE(timestamp)
```

Only two models required SQL modification:

- dim_date.sql
- int_delivery_metrics.sql

All remaining models worked without changes.

---

# Validation

## dbt debug

Purpose

Validate connection to BigQuery.

Result

```
Connection successful
```

---

## dbt compile

Purpose

Compile every model before execution.

Result

```
26 models compiled successfully
```

---

## dbt run

Purpose

Build warehouse models.

Created

```
16 Views

10 Tables
```

Result

```
26 Models

Completed Successfully
```

---

## dbt test

Purpose

Validate warehouse quality.

Executed

```
32 Tests
```

Types

- unique
- not_null
- relationships

Result

```
PASS = 32

WARN = 0

ERROR = 0
```

---

# Final Warehouse

```
olist_raw

├── Raw Tables
│
▼

olist_analytics

Views

stg_*

int_*

Tables

dim_*

fact_*

executive_dashboard
```

---

# Current Pipeline

```
Kaggle + Weather API

↓

Python ETL

↓

Google Cloud Storage

↓

BigQuery Raw

↓

dbt

↓

Analytics Warehouse
```

---

# Files Modified

```
dbt_project.yml

profiles.yml

models/staging/sources.yml

models/intermediate/int_delivery_metrics.sql

models/marts/dim_date.sql
```

---

# Key Lessons Learned

- Separate raw and analytics datasets.
- Use dbt to organize transformations into layers.
- Use Views for staging and intermediate models.
- Use Tables for marts to improve dashboard performance.
- Use `identifier` mapping instead of renaming source tables.
- Test every model before exposing data to dashboards.
- Small SQL syntax differences exist between DuckDB and BigQuery when migrating projects.

---

# Deliverables

- BigQuery warehouse implemented
- dbt configured for BigQuery
- 26 transformation models built successfully
- 32 automated data quality tests passed
- Analytics dataset ready for Power BI

---

# Next Phase

## Phase 07 – Airflow + dbt Orchestration

Goal

```
Python ETL

↓

Upload to GCS

↓

Load BigQuery Raw

↓

dbt run

↓

dbt test

↓

Analytics Warehouse Updated Automatically
```