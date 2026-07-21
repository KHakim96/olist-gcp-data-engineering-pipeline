"""
Infer BigQuery Schemas from Olist CSV Files.

Responsibilities
----------------
1. Read every CSV inside data/raw/olist.
2. Infer BigQuery data types.
3. Generate JSON schema files.
4. Save schemas into schemas/olist.
"""

from pathlib import Path
import json

import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

RAW_DATA_DIR = Path("data/raw/olist")
SCHEMA_DIR = Path("schemas/olist")

SCHEMA_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Data Type Mapping
# ==========================================================


def infer_bigquery_type(dtype) -> str:
    """
    Convert Pandas dtype into BigQuery type.
    """

    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"

    if pd.api.types.is_float_dtype(dtype):
        return "FLOAT"

    if pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"

    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"

    return "STRING"


# ==========================================================
# Schema Generation
# ==========================================================


def generate_schema(csv_file: Path):

    dataframe = pd.read_csv(csv_file)

    schema = []

    for column in dataframe.columns:

        schema.append(
            {
                "name": column,
                "type": infer_bigquery_type(dataframe[column].dtype),
                "mode": "NULLABLE",
            }
        )

    output_file = SCHEMA_DIR / f"{csv_file.stem}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(schema, file, indent=4)

    print(f"✔ {csv_file.name}")


# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("BigQuery Schema Generator")
    print("=" * 70)

    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    for csv_file in csv_files:
        generate_schema(csv_file)

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)
    print(f"Schemas Generated : {len(csv_files)}")
    print(f"Output            : {SCHEMA_DIR.resolve()}")


if __name__ == "__main__":
    main()
