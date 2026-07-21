"""
Load historical weather JSON into BigQuery.
"""

from google.cloud import bigquery

PROJECT_ID = "olist-gcp-data-engineering"

DATASET = "olist_raw"

TABLE = "weather_historical"

FILE = "data/raw/weather/weather_historical.json"

client = bigquery.Client(project=PROJECT_ID)


def main():

    print("=" * 70)
    print("Load Historical Weather")
    print("=" * 70)

    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(FILE, "rb") as source:

        job = client.load_table_from_file(
            source,
            table_id,
            job_config=job_config,
        )

    job.result()

    table = client.get_table(table_id)

    print(f"Rows : {table.num_rows:,}")

    print("Completed")


if __name__ == "__main__":
    main()
