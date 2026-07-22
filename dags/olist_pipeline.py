"""
Olist GCP Data Engineering Pipeline

End-to-end pipeline

Kaggle
    ↓
Weather API
    ↓
Schema Generation
    ↓
Google Cloud Storage
    ↓
BigQuery Raw Layer
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# ==========================================================
# Import Pipeline Tasks
# ==========================================================

from scripts.sources.kaggle.download_olist_dataset import (
    main as download_olist_dataset,
)

from scripts.sources.weather.fetch_weather_api import (
    main as fetch_weather_api,
)

from scripts.schemas.infer_bigquery_schema import (
    main as infer_olist_schema,
)

from scripts.schemas.infer_weather_schema import (
    main as infer_weather_schema,
)

from scripts.gcs.upload_olist_to_gcs import (
    main as upload_olist_to_gcs,
)

from scripts.gcs.upload_weather_to_gcs import (
    main as upload_weather_to_gcs,
)

from scripts.bigquery.create_datasets import (
    main as create_bigquery_datasets,
)

from scripts.bigquery.create_tables import (
    main as create_bigquery_tables,
)

from scripts.bigquery.load_olist_to_bigquery import (
    main as load_olist_to_bigquery,
)

from scripts.bigquery.load_weather_to_bigquery import main as load_weather_to_bigquery

# ==========================================================
# Default Arguments
# ==========================================================

default_args = {
    "owner": "Luqman",
    "depends_on_past": False,
    "retries": 2,
}

# ==========================================================
# DAG
# ==========================================================

with DAG(
    dag_id="olist_gcp_data_engineering_pipeline",
    description="End-to-End Olist GCP Data Engineering Pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=[
        "gcp",
        "bigquery",
        "gcs",
        "airflow",
        "dbt",
        "olist",
    ],
) as dag:

    # ======================================================
    # Start / End
    # ======================================================

    start = EmptyOperator(task_id="start")

    end = EmptyOperator(task_id="end")

    # ======================================================
    # Source
    # ======================================================

    task_download_olist = PythonOperator(
        task_id="download_olist_dataset",
        python_callable=download_olist_dataset,
    )

    task_fetch_weather = PythonOperator(
        task_id="fetch_weather_api",
        python_callable=fetch_weather_api,
    )

    # ======================================================
    # Schema
    # ======================================================

    task_infer_olist_schema = PythonOperator(
        task_id="infer_olist_schema",
        python_callable=infer_olist_schema,
    )

    task_infer_weather_schema = PythonOperator(
        task_id="infer_weather_schema",
        python_callable=infer_weather_schema,
    )

    # ======================================================
    # GCS
    # ======================================================

    task_upload_olist = PythonOperator(
        task_id="upload_olist_to_gcs",
        python_callable=upload_olist_to_gcs,
    )

    task_upload_weather = PythonOperator(
        task_id="upload_weather_to_gcs",
        python_callable=upload_weather_to_gcs,
    )

    # ======================================================
    # BigQuery
    # ======================================================

    task_create_datasets = PythonOperator(
        task_id="create_bigquery_datasets",
        python_callable=create_bigquery_datasets,
    )

    task_create_tables = PythonOperator(
        task_id="create_bigquery_tables",
        python_callable=create_bigquery_tables,
    )

    task_load_olist = PythonOperator(
        task_id="load_olist_to_bigquery",
        python_callable=load_olist_to_bigquery,
    )

    task_load_weather = PythonOperator(
        task_id="load_weather_to_bigquery",
        python_callable=load_weather_to_bigquery,
    )

    # ======================================================
    # Dependencies
    # ======================================================

    (
        start
        >> task_download_olist
        >> task_fetch_weather
        >> task_infer_olist_schema
        >> task_infer_weather_schema
        >> task_upload_olist
        >> task_upload_weather
        >> task_create_datasets
        >> task_create_tables
        >> task_load_olist
        >> task_load_weather
        >> end
    )
