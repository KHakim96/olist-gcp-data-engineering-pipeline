# ⚡ Olist E-Commerce GCP Data Engineering & Executive Analytics Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud Platform](https://img.shields.io/badge/GCP-BigQuery%20%7C%20GCS%20%7C%20GCE-4285F4.svg?logo=google-cloud)](https://cloud.google.com/)
[![dbt Core](https://img.shields.io/badge/dbt-1.12%20Core-FF694B.svg?logo=dbt)](https://www.getdbt.com/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-2.x%20Docker-017CEE.svg?logo=apache-airflow)](https://airflow.apache.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, end-to-end ELT data pipeline and executive intelligence platform built on **Google Cloud Platform (GCP)**. This system processes ~100k real-world Brazilian e-commerce orders (Olist dataset) alongside external weather data, transforms raw transactional data into a dimensional star-schema warehouse using **dbt**, orchestrates complex workflows via **Apache Airflow** on Docker, and serves interactive executive insights through a **Streamlit** Web Application.

---

## 📌 1. Project Title & Executive Summary

### Executive Overview
In modern e-commerce enterprises, converting raw operational logs into actionable executive intelligence requires a robust, scalable, and automated data engineering platform. This project implements a production-ready **ELT (Extract, Load, Transform)** architecture designed to solve key business challenges:

- **Unified Ingestion**: Seamlessly ingests structured relational data (100k+ orders, customers, products, payments, reviews) and semi-structured external REST API data (historical weather).
- **Scalable Storage & Warehousing**: Leverages **Google Cloud Storage (GCS)** as a central Data Lake and **Google BigQuery** as a high-performance Data Warehouse.
- **Analytics Engineering**: Employs **dbt Core** to convert raw bronze tables into standardized silver views and gold dimensional star-schema marts (**16 Views, 10 Tables**) backed by 32 automated quality assertions.
- **Automated Workflow Orchestration**: Fully automated DAG execution in **Apache Airflow** running inside containerized Docker environments on a GCP Compute Engine VM.
- **Executive Intelligence Dashboard**: A responsive **Streamlit** dashboard delivering C-suite visibility into revenue trends, order fulfillment bottlenecks, seller performance, and customer geography, complete with dark/light theme switching.

---

## 🏗️ 2. Architecture & Tech Stack

### Data Lifecycle & Architecture Diagram

```
                       ┌─────────────────────────────────────────────────────────┐
                       │                     DATA SOURCES                        │
                       │  • Olist E-Commerce CSVs (Kaggle API)                   │
                       │  • Historical Weather API (Open-Meteo REST API)         │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
                                                    ▼
                       ┌─────────────────────────────────────────────────────────┐
                       │               INGESTION & RAW DATA LAKE                 │
                       │  • Python Ingestion & Schema Inference Scripts          │
                       │  • Google Cloud Storage (GCS Data Lake Bucket)          │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
                                                    ▼
                       ┌─────────────────────────────────────────────────────────┐
                       │            DATA WAREHOUSE (BIGQUERY RAW LAYER)          │
                       │  • Dataset: `olist_raw`                                 │
                       │  • Raw Landing Tables (CSV & JSON Ingestion)            │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
                                                    ▼
                       ┌─────────────────────────────────────────────────────────┐
                       │          ANALYTICS ENGINEERING (dbt CORE LAYER)         │
                       │  • Dataset: `olist_analytics`                           │
                       │  • Staging Layer (9 Views)                              │
                       │  • Intermediate Layer (7 Views)                        │
                       │  • Marts Layer (10 Tables: Dims, Facts, Executive wide) │
                       │  • Quality Assertions: 32 Passed Automated dbt Tests    │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
                                      ┌─────────────┴─────────────┐
                                      ▼                           ▼
       ┌───────────────────────────────────────────┐ ┌───────────────────────────────────────────┐
       │         ORCHESTRATION & COMPUTE           │ │      EXECUTIVE INTELLIGENCE LAYER        │
       │  • Apache Airflow (Docker Compose)        │ │  • Streamlit Web App (`app.py`)           │
       │  • GCP Compute Engine (Ubuntu VM)         │ │  • Plotly Interactive Visualizations      │
       │  • DAG: `olist_gcp_data_engineering_pip...`│ │  • Dynamic Dark/Light Mode Themes         │
       └───────────────────────────────────────────┘ └───────────────────────────────────────────┘
```

### Technology Stack Components

| Layer | Component | Description & Role |
| :--- | :--- | :--- |
| **Cloud Platform** | **Google Cloud Platform (GCP)** | Core infrastructure host providing IAM, Compute, Storage, and Data Warehousing. |
| **Compute Engine** | **GCP E2 Virtual Machine** | Ubuntu 24.04 LTS VM hosting the Docker container environment and Airflow services. |
| **Data Lake** | **Google Cloud Storage (GCS)** | Object storage bucket (`olist-gcp-data-lake-luqman`) acting as the raw data staging layer. |
| **Data Warehouse** | **Google BigQuery** | Serverless analytical warehouse storing raw (`olist_raw`) and transformed (`olist_analytics`) tables. |
| **Analytics Engineering** | **dbt Core (`dbt-bigquery`)** | Version-controlled SQL transformations, DAG dependencies, model materializations, and data tests. |
| **Orchestration** | **Apache Airflow** | Workflow orchestration executing Python ingestion, GCS upload, BigQuery loads, and dbt execution. |
| **Containerization** | **Docker & Docker Compose** | Isolated multi-container environment housing Airflow Webserver, Scheduler, Worker, and Postgres backend. |
| **Executive UI** | **Streamlit & Plotly** | High-performance interactive dashboard (`app.py`) presenting real-time business metrics and analytics. |

---

## 🛠️ 3. dbt Data Transformation & Modeling

The transformation pipeline converts raw, unvalidated tables into clean, high-performance dimensional models using **dbt Core**.

```
[Raw Tables] ──> (Staging Views: 9) ──> (Intermediate Views: 7) ──> [Mart Tables: 10]
```

### 1. Staging Layer (9 Views)
Staging models clean column names, cast data types, and map raw source identifiers without adding complex joins or aggregations.
- `stg_customers`: Customer identifiers, zip codes, cities, and Brazilian states.
- `stg_orders`: Order IDs, customer references, status flags, and timestamps (purchase, approved, delivered, estimated).
- `stg_order_items`: Line-item details, product keys, seller keys, price, and shipping freight values.
- `stg_order_payments`: Payment types, installment counts, and payment monetary values.
- `stg_order_reviews`: Customer review ratings (1-5 stars) and timestamp metrics.
- `stg_products`: Product dimensions, weight, category names, and photo attributes.
- `stg_sellers`: Seller location mapping and state dimensions.
- `stg_geolocation`: Geolocation lat/long coordinates mapped to zip code prefixes.
- `stg_category_translation`: Portuguese to English translation mappings for product categories.

### 2. Intermediate Layer (7 Views)
Intermediate models encapsulate reusable business logic and derived metric calculations without incurring warehouse storage costs:
- `int_orders`: Base order duration metrics and state flags.
- `int_customer_orders`: Customer purchase frequency, lifetime order counts, and total spend metrics.
- `int_delivery_metrics`: Delivery performance KPIs including actual delivery days, shipping lead times, and fulfillment delay days calculated via BigQuery native `DATE_DIFF`.
- `int_payment_summary`: Aggregated payment metrics per order across credit card, boleto, voucher, and debit options.
- `int_product_sales`: Item sales volumes, revenue generation, and average price per product.
- `int_review_metrics`: Aggregated review scores and feedback response latency per order.
- `int_order_items`: Joined order item attributes enriched with product categories and seller origins.

### 3. Marts Layer (10 Tables)
The final production layer materializes dimensional star-schema models directly into BigQuery tables (`olist_analytics`) to ensure rapid sub-second query performance for BI and Streamlit dashboard tools:
- **Dimension Tables**:
  - `dim_customer`: Unique customer profiles with geographic attributes.
  - `dim_product`: Catalog items enriched with translated category names and physical specifications.
  - `dim_seller`: Active seller directory with location metadata.
  - `dim_geolocation`: Deduplicated geographic coordinates mapped across Brazilian states.
  - `dim_date`: Complete calendar dimension generated for temporal drill-downs.
- **Fact Tables**:
  - `fact_orders`: Granular order header facts containing status, timestamps, and delivery KPIs.
  - `fact_order_items`: Detailed line-item transactional facts with price and freight breakdown.
  - `fact_payments`: Financial transaction facts detailing payment modes and installment breakdowns.
  - `fact_reviews`: Satisfaction metrics and customer rating facts.
- **Wide Analytics Model**:
  - `executive_dashboard`: Pre-aggregated wide table merging orders, customer location, logistics speed, and financial revenue for instant executive querying.

### 🧪 Data Quality & Automated Testing
Data integrity is strictly validated before deployment. Running `dbt test` executes **32 automated quality assertions**:
- **Primary Key Uniqueness**: Verified across all dimension and fact entities (`unique`).
- **Null Value Constraints**: Enforced on essential keys, timestamps, and monetary figures (`not_null`).
- **Referential Integrity**: Validated via foreign key relationship tests (`relationships`).

```text
dbt Test Execution Results:
─────────────────────────────────────────────────────────────
PASS=32  WARN=0  ERROR=0  TOTAL=32 (100% Quality Pass Rate)
─────────────────────────────────────────────────────────────
```

---

## ⚙️ 4. Orchestration & Workflow

Pipeline workflows are orchestrated end-to-end by **Apache Airflow** using the DAG `olist_gcp_data_engineering_pipeline`.

```
[Start]
   │
   ├─► Download Olist Kaggle CSVs ──► Fetch Weather REST API
   │
   ├─► Infer BigQuery Schemas (Olist & Weather)
   │
   ├─► Upload Raw Files to GCS Data Lake
   │
   ├─► Create BigQuery Datasets & Tables ──► Load Raw Data to `olist_raw`
   │
   ├─► Execute `dbt run`  (Materialize 16 Views & 10 Tables in `olist_analytics`)
   │
   ├─► Execute `dbt test` (Validate 32 Data Quality Rules)
   │
[End]
```

### Airflow Task Dependency Graph

1. **`download_olist_dataset`** (`PythonOperator`): Fetches raw e-commerce CSVs from Kaggle into local staging storage.
2. **`fetch_weather_api`** (`PythonOperator`): Calls the Open-Meteo REST API to retrieve historical weather observations.
3. **`infer_olist_schema` & `infer_weather_schema`** (`PythonOperator`): Dynamically builds BigQuery JSON schema definitions from ingested datasets.
4. **`upload_olist_to_gcs` & `upload_weather_to_gcs`** (`PythonOperator`): Pushes raw files into the GCS bucket (`olist-gcp-data-lake-luqman`).
5. **`create_bigquery_datasets` & `create_bigquery_tables`** (`PythonOperator`): Provisions `olist_raw` and `olist_analytics` datasets in BigQuery.
6. **`load_olist_to_bigquery` & `load_weather_to_bigquery`** (`PythonOperator`): Loads raw CSV/JSON files from GCS into BigQuery landing tables.
7. **`dbt_run`** (`BashOperator`): Triggers `dbt run` inside `/opt/airflow/dbt_olist` to execute all 26 models in dependency order.
8. **`dbt_test`** (`BashOperator`): Triggers `dbt test` to execute data quality assertion suites.

### DAG Configuration Details
- **Schedule Interval**: `None` (Manual trigger) or configurable cron `0 2 * * *` (Daily at 02:00 UTC).
- **Execution Policy**: `catchup=False`, `depends_on_past=False`, `retries=2`.

---

## 📊 5. Executive Streamlit Dashboard

The project includes an executive-facing interactive analytics web application built with **Streamlit** and **Plotly** (`app.py`).

### Key Executive Metrics (KPI Ribbon)
- 💰 **Total Revenue**: Total gross merchandise value (GMV in BRL).
- 📦 **Total Orders**: Total volume of customer orders processed.
- 💳 **Avg Order Value (AOV)**: Mean monetary spend per completed transaction.
- ⚡ **Delivery On-Time Rate**: Percentage of orders delivered on or before the estimated delivery date.
- 🚚 **Avg Freight Cost**: Mean shipping fee per order.
- ⭐ **Avg Review Rating**: Average customer satisfaction score (out of 5 stars).
- 🏬 **Active Sellers**: Count of active merchants selling on the platform.

### Dashboard Analytics Modules (Tabs)
1. 📈 **Executive Revenue & Orders**: Monthly revenue trends, order volume trajectory, and payment breakdown by category (Credit Card, Boleto, Voucher, Debit).
2. 🚚 **Logistics & Operations**: Delivery duration distributions, carrier shipping lead times, fulfillment delay analysis, and freight cost breakdown across Brazilian states.
3. 👤 **Customer & Geographics**: State-wise customer distribution, regional order density across Brazil, and geographic seller concentrations.
4. 🛠️ **dbt Marts & Pipeline Architecture**: Interactive explorer allowing users to inspect raw dbt data marts (`executive_dashboard`, `fact_orders`, `dim_customer`), inspect data schemas, and review pipeline lineage.

### Advanced Design & User Experience Features
- **Dynamic Dark / Light Mode Toggle**: Seamlessly switches UI palette, typography, chart backgrounds, card shadows, and borders in real-time.
- **Glassmorphism & Gradient UI**: Styled with custom CSS headers, polished metric cards, responsive container padding, and modern typography.

---

## 🚀 6. Setup & Local Deployment Guide

### Prerequisites
- **Python 3.10+**
- **Docker & Docker Compose** (for running Airflow)
- **GCP Account** with an active GCP Project, GCS Bucket, and BigQuery enabled.
- **GCP Service Account JSON Key** with BigQuery Admin and Storage Admin privileges.

---

### Step 1: Clone Repository & Create Virtual Environment
```bash
# Clone the repository
git clone https://github.com/KHakim96/olist-gcp-data-engineering-pipeline.git
cd olist-gcp-data-engineering-pipeline

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

---

### Step 2: Configure GCP Service Account Credentials
1. Place your GCP Service Account JSON key file inside the `config/` directory:
   ```bash
   cp /path/to/your-service-account-key.json config/service-account.json
   ```
2. Set the environment variable in your terminal:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/config/service-account.json"
   ```

---

### Step 3: Run dbt Transformations & Tests (Local Mode)
```bash
# Navigate to dbt project directory
cd dbt_olist

# Test BigQuery connection setup
dbt debug

# Execute dbt model transformations
dbt run

# Run automated data quality tests
dbt test

# Return to root directory
cd ..
```

---

### Step 4: Launch Airflow via Docker Compose
```bash
# Build and start containerized Airflow services
docker compose up -d --build

# Verify running containers
docker compose ps
```
- Open your browser and navigate to **Airflow Web UI**: `http://localhost:8080` (Credentials: `airflow` / `airflow`).
- Trigger the DAG `olist_gcp_data_engineering_pipeline` to run the full ingestion and dbt pipeline.

---

### Step 5: Launch Executive Streamlit Dashboard
```bash
# Start the Streamlit application
streamlit run app.py
```
- Access the web interface at `http://localhost:8501`.

---

## 📁 7. Repository Structure

```text
olist-gcp-data-engineering-pipeline/
├── .streamlit/
│   └── config.toml                 # Streamlit server & theme configuration
├── config/
│   └── service-account.json        # GCP Service Account key (git-ignored)
├── dags/
│   └── olist_pipeline.py           # Master Airflow DAG definition
├── data/                           # Local staging directory for Kaggle & API data
│   ├── raw/
│   └── schemas/
├── dbt_olist/                      # dbt Analytics Engineering project
│   ├── dbt_project.yml             # dbt project configurations & materialization rules
│   ├── profiles.yml                # BigQuery profile connection settings
│   ├── macros/                     # Custom dbt macros
│   ├── tests/                      # Custom data assertions
│   └── models/                     # dbt SQL transformation models
│       ├── staging/                # 9 Staging Views (`stg_*`)
│       ├── intermediate/           # 7 Intermediate Views (`int_*`)
│       └── marts/                  # 10 Mart Tables (`dim_*`, `fact_*`, `executive_*`)
├── docs/                           # Architectural diagrams and design specifications
├── notes/                          # Detailed phase-by-phase engineering documentation
│   ├── 00_project_planning.md
│   ├── 01_gcp_setup.md
│   ├── 02_compute_engine_airflow.md
│   ├── 03_cloud_storage.md
│   ├── 04_bigquery_raw.md
│   ├── 05_airflow_pipeline.md
│   ├── 06_dbt_transformations.md
│   └── 07_airflow_dbt_orchestration.md
├── plugins/                        # Airflow custom plugins directory
├── scripts/                        # Modular Python ETL execution scripts
│   ├── bigquery/                   # Dataset creation & raw loading modules
│   ├── gcs/                        # Cloud storage upload modules
│   ├── schemas/                    # Automated schema inference utilities
│   ├── sources/                    # Kaggle CSV & Weather API fetchers
│   └── utilities/                  # Logging and GCP client helpers
├── .env                            # Environment variables config
├── .gitignore                      # Git ignore file rules
├── app.py                          # Streamlit Executive Dashboard Web Application
├── Dockerfile                      # Airflow Docker build instructions
├── docker-compose.yml              # Multi-container orchestration specification
├── requirements.txt                # Python package dependency manifest
└── README.md                       # Project documentation
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
