# Phase 03 – Google Cloud Storage

## Objective

The objective of this phase is to build the Data Lake layer of the project using Google Cloud Storage (GCS).

Two independent data sources are ingested:

- Internal transactional data (Olist E-Commerce Dataset)
- External historical weather data (Open-Meteo API)

Both datasets are stored in Google Cloud Storage before being loaded into BigQuery.

This follows the common cloud data engineering architecture:

Source Systems

↓

Data Lake

↓

Data Warehouse

↓

Analytics

---

# Architecture

                Google Cloud Storage

            ┌──────────────────────────────┐
            │                              │
            │      Data Lake (Raw Zone)    │
            │                              │
            └──────────────┬───────────────┘
                           │
          ┌────────────────┴───────────────┐
          │                                │
          ▼                                ▼

Kaggle Olist Dataset             Open-Meteo Historical API

---

# Google Cloud Storage Bucket

Bucket Name

olist-gcp-data-lake-luqman

Folder Structure

gs://olist-gcp-data-lake-luqman/

├── olist/
│   └── raw/
│
│       ├── olist_customers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       └── product_category_name_translation.csv
│
└── weather/
    └── raw/
        └── weather_historical.json

---

# Local Folder Structure

data/

├── raw/
│
├── olist/
│
│   ├── olist_customers_dataset.csv
│   ├── ...
│
└── weather/
    └── weather_historical.json

---

# Scripts

scripts/

├── sources/
│
│   ├── kaggle/
│   │
│   └── download_olist_dataset.py
│
│   └── weather/
│
│       └── fetch_weather_api.py
│
├── gcs/
│
├── upload_olist_to_gcs.py
│
└── upload_weather_to_gcs.py

---

# Step 1

Download Olist Dataset

File

scripts/sources/kaggle/download_olist_dataset.py

Purpose

Automatically download the Olist dataset from Kaggle.

Package Used

kagglehub

Implementation

Downloads

Brazilian E-Commerce Public Dataset

Copies every CSV file into

data/raw/olist/

The script first checks whether the dataset already exists.

If the files are present, the download is skipped.

Benefits

Avoids unnecessary downloads.

Supports repeated execution.

Output

9 CSV files

---

# Downloaded Tables

- Customers
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Category Translation

---

# Step 2

Generate BigQuery Schemas

File

scripts/schemas/infer_bigquery_schema.py

Purpose

Automatically infer BigQuery schemas from every CSV file.

Implementation

Reads every CSV file.

Detects

Column Names

Column Types

Outputs JSON schemas into

schemas/olist_raw/

Benefits

No manual schema creation.

Reusable during table creation.

Automatically adapts to future datasets.

---

# Step 3

Historical Weather Data

File

scripts/sources/weather/fetch_weather_api.py

Purpose

Collect historical weather data covering the same time period as the Olist dataset.

Instead of downloading today's weather, the script dynamically determines the required historical period.

Implementation

Reads

olist_orders_dataset.csv

Extracts

Minimum order date

Maximum order date

Result

Start Date

2016-09-04

End Date

2018-10-17

The script requests historical daily weather data for ten major Brazilian cities.

Cities

- Sao Paulo
- Rio de Janeiro
- Brasilia
- Salvador
- Fortaleza
- Belo Horizonte
- Curitiba
- Manaus
- Recife
- Porto Alegre

Weather Variables

- Maximum Temperature
- Minimum Temperature
- Daily Precipitation
- Rainfall
- Weather Code

API Used

Open-Meteo Archive API

Output Format

NDJSON

(Newline Delimited JSON)

Reason

BigQuery directly supports NDJSON.

Output File

data/raw/weather/weather_historical.json

Records

7,740

---

# Why Historical Weather?

Using historical weather makes the external dataset align with the Olist transaction dates.

Instead of comparing 2017 sales with today's weather, every weather record corresponds to the historical period covered by the Olist dataset.

This creates a realistic external enrichment dataset for future analytics.

Examples

Relationship between rainfall and sales

Relationship between temperature and delivery performance

Weather impact on customer reviews

Weather impact on purchasing behaviour

---

# Step 4

Generate Weather Schema

File

scripts/schemas/infer_weather_schema.py

Purpose

Automatically infer the BigQuery schema from the historical weather dataset.

Implementation

Reads the first NDJSON record.

Determines

Column Name

Column Type

Outputs

schemas/olist_raw/weather_historical.json

Benefits

No manual schema writing.

Automatically updates when new weather attributes are added.

---

# Step 5

Upload Olist Dataset

File

scripts/gcs/upload_olist_to_gcs.py

Purpose

Upload every Olist CSV into Google Cloud Storage.

Destination

gs://olist-gcp-data-lake-luqman/olist/raw/

Implementation

Automatically scans

data/raw/olist/

Uploads every CSV file.

If the file already exists in the bucket, the upload is skipped.

Benefits

Idempotent execution.

No duplicate uploads.

---

# Step 6

Upload Historical Weather

File

scripts/gcs/upload_weather_to_gcs.py

Purpose

Upload the historical weather dataset into Google Cloud Storage.

Destination

gs://olist-gcp-data-lake-luqman/weather/raw/

Implementation

Uploads

weather_historical.json

Checks if the object already exists.

Skips upload if present.

---

# Final Google Cloud Storage Structure

gs://olist-gcp-data-lake-luqman/

├── olist/
│   └── raw/
│
│       ├── olist_customers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       └── product_category_name_translation.csv
│
└── weather/
    └── raw/
        └── weather_historical.json

---

# Challenges

Issue

Originally implemented current weather API.

Problem

Current weather could not be related to historical Olist transactions.

Solution

Replaced with Open-Meteo Historical Archive API.

---

Issue

Historical weather initially saved as a JSON array.

Problem

BigQuery expects NDJSON for JSON loading.

Solution

Modified the weather downloader to write one JSON object per line.

---

Issue

Weather schema generator expected a JSON array.

Solution

Updated the schema generator to infer the schema from the first NDJSON record.

---

# Idempotency

Every script is safe to execute multiple times.

Download

Skips if dataset already exists.

Weather Fetch

Overwrites the local weather dataset.

Schema Generation

Overwrites schema JSON.

Olist Upload

Skips existing GCS objects.

Weather Upload

Skips existing GCS object.

No duplicate files are produced.

---

# Deliverables

Completed

✓ Olist dataset downloaded

✓ BigQuery schemas generated

✓ Historical weather dataset collected

✓ Weather schema generated

✓ Olist uploaded to Google Cloud Storage

✓ Weather uploaded to Google Cloud Storage

✓ Cloud Data Lake completed

---

# Status

✅ Completed