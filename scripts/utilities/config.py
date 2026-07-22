"""
Central Project Configuration
"""

from pathlib import Path
import os

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(
    os.getenv(
        "PROJECT_ROOT",
        Path(__file__).resolve().parents[2],
    )
)


# ==========================================================
# GCP
# ==========================================================

PROJECT_ID = os.getenv(
    "GOOGLE_CLOUD_PROJECT",
    "olist-gcp-data-engineering",
)

GCS_BUCKET = os.getenv(
    "GCS_BUCKET",
    "olist-gcp-data-lake-luqman",
)

BQ_RAW_DATASET = os.getenv(
    "BQ_RAW_DATASET",
    "olist_raw",
)

BQ_ANALYTICS_DATASET = os.getenv(
    "BQ_ANALYTICS_DATASET",
    "olist_analytics",
)


# ==========================================================
# Directories
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"

OLIST_RAW_DIR = RAW_DIR / "olist"

WEATHER_RAW_DIR = RAW_DIR / "weather"

SCHEMA_DIR = PROJECT_ROOT / "schemas"

SCRIPTS_DIR = PROJECT_ROOT / "scripts"

CONFIG_DIR = PROJECT_ROOT / "config"


# ==========================================================
# Files
# ==========================================================

ORDERS_FILE = OLIST_RAW_DIR / "olist_orders_dataset.csv"

WEATHER_FILE = WEATHER_RAW_DIR / "weather_historical.json"
