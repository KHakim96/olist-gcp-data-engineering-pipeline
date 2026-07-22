"""
Upload Historical Weather Data to Google Cloud Storage.
"""

from google.cloud import storage

from scripts.utilities.config import (
    PROJECT_ID,
    GCS_BUCKET,
    WEATHER_FILE,
)

# ==========================================================
# Configuration
# ==========================================================

LOCAL_FILE = WEATHER_FILE

DESTINATION = "weather/raw/weather_historical.json"

# ==========================================================
# GCS Client
# ==========================================================

client = storage.Client(project=PROJECT_ID)

bucket = client.bucket(GCS_BUCKET)

# ==========================================================
# Upload
# ==========================================================


def main():

    print("=" * 70)
    print("Upload Historical Weather")
    print("=" * 70)

    blob = bucket.blob(DESTINATION)

    if blob.exists(client):

        print("Weather dataset already exists.")
        print("Skipping upload.")

        return

    blob.upload_from_filename(LOCAL_FILE)

    print()
    print("=" * 70)
    print("Upload Completed")
    print("=" * 70)
    print(f"Bucket      : {GCS_BUCKET}")
    print(f"Destination : gs://{GCS_BUCKET}/{DESTINATION}")


if __name__ == "__main__":
    main()
