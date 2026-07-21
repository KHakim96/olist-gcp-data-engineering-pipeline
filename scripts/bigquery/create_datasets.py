"""
Create required BigQuery datasets.
"""

from google.cloud import bigquery

PROJECT_ID = "olist-gcp-data-engineering"

DATASETS = [
    "olist_raw",
    "olist_analytics",
]


def main():

    client = bigquery.Client(project=PROJECT_ID)

    print("=" * 70)
    print("Create BigQuery Datasets")
    print("=" * 70)

    for dataset in DATASETS:

        dataset_id = f"{PROJECT_ID}.{dataset}"

        obj = bigquery.Dataset(dataset_id)
        obj.location = "asia-southeast1"

        client.create_dataset(obj, exists_ok=True)

        print(f"✓ {dataset}")

    print()
    print("Completed")


if __name__ == "__main__":
    main()
