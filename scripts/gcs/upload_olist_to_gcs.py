"""
Upload Olist CSV files to Google Cloud Storage.

Responsibilities
----------------
1. Read CSV files from data/raw/olist.
2. Upload files to Google Cloud Storage.
3. Skip upload if the object already exists.
"""

from pathlib import Path

from google.cloud import storage

# ==========================================================
# Configuration
# ==========================================================

PROJECT_ID = "olist-gcp-data-engineering"

BUCKET_NAME = "olist-gcp-data-lake-luqman"

LOCAL_DIRECTORY = Path("data/raw/olist")

GCS_PREFIX = "olist/raw"


# ==========================================================
# GCS Client
# ==========================================================

client = storage.Client(project=PROJECT_ID)

bucket = client.bucket(BUCKET_NAME)


# ==========================================================
# Upload
# ==========================================================


def upload_file(file_path: Path):

    blob = bucket.blob(f"{GCS_PREFIX}/{file_path.name}")

    if blob.exists(client):

        print(f"Skipped : {file_path.name}")

        return

    blob.upload_from_filename(file_path)

    print(f"Uploaded : {file_path.name}")


# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("Upload Olist Dataset to Google Cloud Storage")
    print("=" * 70)

    csv_files = sorted(LOCAL_DIRECTORY.glob("*.csv"))

    if not csv_files:

        print("No CSV files found.")

        return

    for csv in csv_files:

        upload_file(csv)

    print()
    print("=" * 70)
    print("Upload Completed")
    print("=" * 70)
    print(f"Bucket : {BUCKET_NAME}")
    print(f"Folder : gs://{BUCKET_NAME}/{GCS_PREFIX}/")


if __name__ == "__main__":
    main()
