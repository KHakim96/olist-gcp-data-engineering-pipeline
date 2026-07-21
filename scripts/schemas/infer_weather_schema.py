"""
Infer BigQuery schema from historical weather JSON.
"""

from pathlib import Path
import json

INPUT_FILE = Path("data/raw/weather/weather_historical.json")

OUTPUT_FILE = Path("schemas/weather/weather_historical.json")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


TYPE_MAPPING = {
    str: "STRING",
    int: "INTEGER",
    float: "FLOAT",
    bool: "BOOLEAN",
}


def infer_type(value):

    if value is None:
        return "STRING"

    return TYPE_MAPPING.get(type(value), "STRING")


def main():

    print("=" * 70)
    print("Infer Weather BigQuery Schema")
    print("=" * 70)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        first_line = f.readline()

    sample = json.loads(first_line)

    schema = []

    for column, value in sample.items():

        schema.append(
            {
                "name": column,
                "type": infer_type(value),
                "mode": "NULLABLE",
            }
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(schema, f, indent=4)

    print()
    print(f"Schema saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
