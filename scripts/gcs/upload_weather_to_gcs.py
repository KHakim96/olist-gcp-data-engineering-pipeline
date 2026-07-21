"""
Upload Historical Weather Data to Google Cloud Storage.
"""

from pathlib import Path

from google.cloud import storage

# ==========================================================
# Configuration
# ==========================================================

PROJECT_ID = "olist-gcp-data-engineering"

BUCKET_NAME = "olist-gcp-data-lake-luqman"

LOCAL_FILE = Path("data/raw/weather/weather_historical.json")

DESTINATION = "weather/raw/weather_historical.json"


# ==========================================================
# Upload
# ==========================================================


def main():

    print("=" * 70)
    print("Upload Historical Weather")
    print("=" * 70)

    client = storage.Client(project=PROJECT_ID)

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(DESTINATION)

    if blob.exists(client):

        print("Weather dataset already exists.")
        print("Skipping upload.")
        return

    blob.upload_from_filename(LOCAL_FILE)

    print("Upload completed.")
    print(f"Bucket      : {BUCKET_NAME}")
    print(f"Destination : gs://{BUCKET_NAME}/{DESTINATION}")


if __name__ == "__main__":
    main()
