from file_manager import *
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def upload_blob(file_path):
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(os.path.basename(file_path))
    with open(file_path, "rb") as data:
        total_size = os.path.getsize(file_path)
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Uploading {os.path.basename(file_path)}") as pbar:
            blob_client.upload_blob(data, raw_response_hook=lambda response: pbar.update(len(response.http_response.body())))
    print(f"File {file_path} uploaded to blob storage.")

def upload_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") or filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                upload_blob(file_path)
            except ResourceExistsError as e:
                print(f"File {filename} already exists in blob storage, skipping.")

if __name__ == "__main__":
    assets_directory = os.path.join(os.getcwd(), "assets")
    upload_files_in_directory(assets_directory)