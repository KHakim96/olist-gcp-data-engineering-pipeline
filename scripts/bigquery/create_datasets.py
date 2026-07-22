"""
Create Required BigQuery Datasets.
"""

from google.cloud import bigquery

from scripts.utilities.config import (
    PROJECT_ID,
    BQ_RAW_DATASET,
    BQ_ANALYTICS_DATASET,
)

# ==========================================================
# Configuration
# ==========================================================

DATASETS = [
    BQ_RAW_DATASET,
    BQ_ANALYTICS_DATASET,
]

LOCATION = "asia-southeast1"

# ==========================================================
# Main
# ==========================================================


def main():

    client = bigquery.Client(project=PROJECT_ID)

    print("=" * 70)
    print("Create BigQuery Datasets")
    print("=" * 70)

    for dataset in DATASETS:

        dataset_id = f"{PROJECT_ID}.{dataset}"

        dataset_obj = bigquery.Dataset(dataset_id)

        dataset_obj.location = LOCATION

        client.create_dataset(
            dataset_obj,
            exists_ok=True,
        )

        print(f"✓ {dataset}")

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)


if __name__ == "__main__":
    main()
