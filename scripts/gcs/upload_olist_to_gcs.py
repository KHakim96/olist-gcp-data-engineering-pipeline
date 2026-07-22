"""
Upload Olist CSV Files to Google Cloud Storage.

Responsibilities
----------------
1. Read CSV files from data/raw/olist.
2. Upload files to Google Cloud Storage.
3. Skip upload if the object already exists.
"""

from google.cloud import storage

from scripts.utilities.config import (
    PROJECT_ID,
    GCS_BUCKET,
    OLIST_RAW_DIR,
)

# ==========================================================
# Configuration
# ==========================================================

LOCAL_DIRECTORY = OLIST_RAW_DIR

GCS_PREFIX = "olist/raw"

# ==========================================================
# GCS Client
# ==========================================================

client = storage.Client(project=PROJECT_ID)

bucket = client.bucket(GCS_BUCKET)

# ==========================================================
# Upload
# ==========================================================


def upload_file(file_path):

    blob = bucket.blob(f"{GCS_PREFIX}/{file_path.name}")

    if blob.exists(client):

        print(f"Skipped  : {file_path.name}")

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

    for csv_file in csv_files:

        upload_file(csv_file)

    print()
    print("=" * 70)
    print("Upload Completed")
    print("=" * 70)
    print(f"Bucket : {GCS_BUCKET}")
    print(f"Folder : gs://{GCS_BUCKET}/{GCS_PREFIX}/")


if __name__ == "__main__":
    main()
