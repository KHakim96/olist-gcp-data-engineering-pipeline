"""
Infer BigQuery Schema from Historical Weather Data.
"""

import json

from scripts.utilities.config import (
    WEATHER_FILE,
    SCHEMA_DIR,
)

# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = WEATHER_FILE

OUTPUT_DIR = SCHEMA_DIR / "olist_raw"

OUTPUT_FILE = OUTPUT_DIR / "weather_historical.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TYPE_MAPPING = {
    str: "STRING",
    int: "INTEGER",
    float: "FLOAT",
    bool: "BOOLEAN",
}


# ==========================================================
# Helper
# ==========================================================


def infer_type(value):

    if value is None:
        return "STRING"

    return TYPE_MAPPING.get(type(value), "STRING")


# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("Infer Weather BigQuery Schema")
    print("=" * 70)

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        sample = json.loads(file.readline())

    schema = []

    for column, value in sample.items():

        schema.append(
            {
                "name": column,
                "type": infer_type(value),
                "mode": "NULLABLE",
            }
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            schema,
            file,
            indent=4,
        )

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)
    print(f"Schema : {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
