"""
Download Olist Dataset from Kaggle.

Responsibilities
----------------
1. Check whether the Olist CSV files already exist.
2. Skip download if all required files are present.
3. Download dataset from Kaggle if missing.
4. Copy CSV files into data/raw/olist.
"""

from pathlib import Path
import shutil

import kagglehub

# ==========================================================
# Configuration
# ==========================================================

DATASET = "jayeshsalunke101/brazilian-ecommerce-public-dataset"

DESTINATION = Path("data/raw/olist")

EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


# ==========================================================
# Helper Functions
# ==========================================================


def dataset_exists() -> bool:
    """Return True if every expected CSV already exists."""

    return all((DESTINATION / file).exists() for file in EXPECTED_FILES)


# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("Olist Dataset Download")
    print("=" * 70)

    DESTINATION.mkdir(parents=True, exist_ok=True)

    if dataset_exists():
        print("Dataset already exists.")
        print(f"Location : {DESTINATION.resolve()}")
        print("Skipping download.")
        return

    print("Downloading dataset from Kaggle...")

    download_path = Path(kagglehub.dataset_download(DATASET))

    copied = 0

    for csv_file in download_path.glob("*.csv"):
        shutil.copy2(csv_file, DESTINATION / csv_file.name)
        copied += 1
        print(f"Copied : {csv_file.name}")

    print()
    print("=" * 70)
    print("Download Completed")
    print("=" * 70)
    print(f"Files copied : {copied}")
    print(f"Destination  : {DESTINATION.resolve()}")


if __name__ == "__main__":
    main()
