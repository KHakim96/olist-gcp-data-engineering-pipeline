"""
Load Historical Weather into BigQuery.
"""

from google.cloud import bigquery

from scripts.utilities.config import (
    PROJECT_ID,
    BQ_RAW_DATASET,
    WEATHER_FILE,
)

# ==========================================================
# Configuration
# ==========================================================

DATASET = BQ_RAW_DATASET

TABLE = "weather_historical"

INPUT_FILE = WEATHER_FILE

client = bigquery.Client(project=PROJECT_ID)

# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("Load Historical Weather")
    print("=" * 70)

    table_id = f"{PROJECT_ID}." f"{DATASET}." f"{TABLE}"

    table = client.get_table(table_id)

    job_config = bigquery.LoadJobConfig(
        schema=table.schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(INPUT_FILE, "rb") as source:

        job = client.load_table_from_file(
            source,
            table_id,
            job_config=job_config,
        )

    try:

        job.result()

    except Exception:

        print("\nFAILED : weather_historical")

        if job.errors:

            for error in job.errors:

                print(error)

        raise

    table = client.get_table(table_id)

    print(f"Rows : {table.num_rows:,}")

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)


if __name__ == "__main__":
    main()
