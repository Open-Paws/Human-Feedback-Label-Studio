import os
import sys
import re
import time
import select
import logging
from google.cloud import storage
from google.auth import default
from tqdm import tqdm

# Constants
TIMEOUT = 10  # Timeout for user input in seconds

# Config
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

# Dictionary of language abbreviations and their full names
# This dictionary is currently commented out but may be used in future implementations
# or in related scripts for language-specific operations
languages = {
    # "en": "English",
    # "es": "Spanish",
    # ... (other languages) ...
    # "af": "Afrikaans"
}

# Setup logging
logging.basicConfig(level=logging.INFO)


def setup_google_cloud():
    """
    Set up Google Cloud authentication and create a storage client.

    Returns:
        storage.Client: Authenticated Google Cloud Storage client
    """
    credentials, project = default()
    return storage.Client(credentials=credentials, project=project)


def is_deletable_file(blob_name):
    """
    Check if a file should be deleted based on its name.

    Args:
        blob_name (str): Name of the blob (file) in Google Cloud Storage

    Returns:
        bool: True if the file is deletable, False otherwise
    """
    pattern = re.compile(r"\.json$")
    return pattern.search(blob_name) and "/" not in blob_name


class BucketOperations:
    """
    A class to handle operations on a Google Cloud Storage bucket.
    """

    def __init__(self, storage_client, bucket_name):
        """
        Initialize BucketOperations with a storage client and bucket name.

        Args:
            storage_client (storage.Client): Google Cloud Storage client
            bucket_name (str): Name of the bucket to operate on
        """
        self.storage_client = storage_client
        self.bucket = self.storage_client.bucket(bucket_name)

    def get_files_to_delete(self):
        """
        Get a list of files in the bucket root that should be deleted.

        Returns:
            list: List of file paths to be deleted
        """
        logging.debug(f"Attempting to list files in the root of {self.bucket.name}")
        files_to_delete = []
        try:
            # In Google Cloud Storage, "blobs" are objects that contain data,
            # which can be thought of as files. Each blob represents an individual
            # file stored in the bucket, including its data and metadata.
            #
            # Note: Folders don't exist as separate entities in GCS. The '/' delimiter
            # is used to simulate a folder structure, but only blobs (files) are actual objects.
            blobs = self.bucket.list_blobs(
                delimiter="/"
            )  # list all blobs in the bucket root
            for blob in blobs:
                if is_deletable_file(blob.name):
                    files_to_delete.append(f"gs://{self.bucket.name}/{blob.name}")
                    logging.debug(f"Added file to delete: {blob.name}")
            logging.debug(f"Found {len(files_to_delete)} files to delete")
        except Exception as e:
            logging.error(f"Error in get_files_to_delete: {str(e)}")
            raise
        return files_to_delete

    def delete_files(self, files_to_delete):
        """
        Delete the specified files from the bucket.

        Args:
            files_to_delete (list): List of file paths to delete
        """
        for file_path in tqdm(files_to_delete, desc="Deleting files", unit="file"):
            blob_name = file_path.split(f"{self.bucket.name}/")[1]
            blob = self.bucket.blob(blob_name)
            try:
                blob.delete()
            except Exception as e:
                logging.error(f"Error deleting {file_path}: {str(e)}")


def input_with_timeout(prompt, timeout):
    """
    Get user input with a timeout.

    Args:
        prompt (str): The prompt to display to the user
        timeout (int): Timeout in seconds

    Returns:
        str: User input or empty string if timeout occurs
    """
    print(prompt, end="", flush=True)
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if rlist:
        return sys.stdin.readline().strip()
    else:
        print("\nNo input received. Auto-confirming...")
        return ""


def confirm_deletion(files_to_delete):
    """
    Ask for user confirmation before deleting files.

    Args:
        files_to_delete (list): List of files to be deleted

    Returns:
        bool: True if deletion is confirmed, False otherwise
    """
    logging.info(f"Number of files pending deletion: {len(files_to_delete)}")
    logging.info("Sample files:")
    for file in files_to_delete[:5]:
        filename = file.split("/")[-1]
        logging.info(f"  - {filename}")
    if len(files_to_delete) > 5:
        logging.info("  ...")

    confirm = input_with_timeout(
        f"Press Enter to confirm deletion of {len(files_to_delete)} files, or type 'skip' to skip (auto-confirms in {TIMEOUT} seconds): ",
        TIMEOUT,
    )

    if confirm.lower() == "skip":
        logging.info("Skipping deletion.")
        return False
    elif confirm == "":  # Empty input (just pressed Enter or timed out)
        return True
    else:
        logging.info("Confirmation failed. Skipping deletion.")
        return False


def main():
    """
    Main function to orchestrate the file deletion process.
    is_deletable_file returns True on any file ending in .json,
    this script will delete all .json files in the root of the bucket.
    """
    try:
        logging.info(f"\nProcessing root of: {BUCKET_NAME}")
        storage_client = setup_google_cloud()
        bucket_ops = BucketOperations(storage_client, BUCKET_NAME)

        files_to_delete = bucket_ops.get_files_to_delete()

        if files_to_delete:
            if confirm_deletion(files_to_delete):
                bucket_ops.delete_files(files_to_delete)
                logging.info("Completed deletion.")
        else:
            logging.info("No files to delete in the root of the bucket.")
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
