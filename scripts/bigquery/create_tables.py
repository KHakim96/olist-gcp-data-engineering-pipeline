"""
Create BigQuery Tables from JSON Schemas.
"""

import json

from google.cloud import bigquery

from scripts.utilities.config import (
    PROJECT_ID,
    SCHEMA_DIR,
)

# ==========================================================
# Configuration
# ==========================================================

SCHEMA_ROOT = SCHEMA_DIR

client = bigquery.Client(project=PROJECT_ID)

# ==========================================================
# Load Schema
# ==========================================================


def load_schema(schema_file):

    with open(schema_file, encoding="utf-8") as file:

        schema_json = json.load(file)

    schema = []

    for column in schema_json:

        schema.append(
            bigquery.SchemaField(
                name=column["name"],
                field_type=column["type"],
                mode=column.get(
                    "mode",
                    "NULLABLE",
                ),
            )
        )

    return schema


# ==========================================================
# Create Tables
# ==========================================================


def create_dataset_tables(dataset_folder):

    dataset = dataset_folder.name

    print()
    print(f"Dataset : {dataset}")

    for schema_file in sorted(dataset_folder.glob("*.json")):

        table_name = schema_file.stem

        table_id = f"{PROJECT_ID}." f"{dataset}." f"{table_name}"

        table = bigquery.Table(
            table_id,
            schema=load_schema(schema_file),
        )

        client.create_table(
            table,
            exists_ok=True,
        )

        print(f"✓ {table_name}")


# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("Create BigQuery Tables")
    print("=" * 70)

    for folder in sorted(SCHEMA_ROOT.iterdir()):

        if folder.is_dir():

            create_dataset_tables(folder)

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)


if __name__ == "__main__":
    main()
