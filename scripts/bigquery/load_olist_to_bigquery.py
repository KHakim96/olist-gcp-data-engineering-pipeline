"""
Load all Olist CSV files into BigQuery.
"""

from pathlib import Path

from google.cloud import bigquery

PROJECT_ID = "olist-gcp-data-engineering"
DATASET = "olist_raw"

DATA_DIR = Path("data/raw/olist")

client = bigquery.Client(project=PROJECT_ID)


def load_csv(csv_file):

    table_name = csv_file.stem

    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    table = client.get_table(table_id)

    job_config = bigquery.LoadJobConfig(
        schema=table.schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        encoding="UTF-8",
        quote_character='"',
        allow_quoted_newlines=True,
    )

    with open(csv_file, "rb") as source:

        job = client.load_table_from_file(
            source,
            table_id,
            job_config=job_config,
        )

    try:
        job.result()
    except Exception:
        print(f"\nFAILED : {table_name}")

        if job.errors:
            for error in job.errors:
                print(error)

        raise

    table = client.get_table(table_id)

    print(f"✓ {table_name:<45}" f"{table.num_rows:>10,} rows")


def main():

    print("=" * 70)
    print("Load Olist CSVs into BigQuery")
    print("=" * 70)

    for csv in sorted(DATA_DIR.glob("*.csv")):

        load_csv(csv)

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)


if __name__ == "__main__":
    main()
