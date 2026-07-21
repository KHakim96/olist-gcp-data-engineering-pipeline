"""
Create BigQuery tables from JSON schema files.
"""

from pathlib import Path
import json

from google.cloud import bigquery

PROJECT_ID = "olist-gcp-data-engineering"

SCHEMA_ROOT = Path("schemas")

client = bigquery.Client(project=PROJECT_ID)


def load_schema(schema_file):

    with open(schema_file, encoding="utf-8") as f:
        schema_json = json.load(f)

    schema = []

    for column in schema_json:

        schema.append(
            bigquery.SchemaField(
                name=column["name"],
                field_type=column["type"],
                mode=column.get("mode", "NULLABLE"),
            )
        )

    return schema


def create_dataset_tables(dataset_folder):

    dataset = dataset_folder.name

    print()
    print(f"Dataset : {dataset}")

    for schema_file in sorted(dataset_folder.glob("*.json")):

        table_name = schema_file.stem

        table_id = f"{PROJECT_ID}.{dataset}.{table_name}"

        table = bigquery.Table(
            table_id,
            schema=load_schema(schema_file),
        )

        client.create_table(table, exists_ok=True)

        print(f"✓ {table_name}")


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
