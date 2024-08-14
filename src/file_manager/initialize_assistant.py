from azure.storage.blob import BlobServiceClient
from file_manager import *
import os, time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def list_blobs_in_container():
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    return [blob.name for blob in blob_list]

def create_pinecone_assistant(asst_name):
    metadata = {"application": "AZD Template example", "version": "0.1"}
    try:
        assistant = pc.assistant.create_assistant(
            assistant_name=asst_name,
            metadata=metadata, 
            timeout=30  # Wait 30 seconds for assistant operation to complete.
        )
        return assistant
    except Exception as e:
        print(f"Exception when creating assistant {asst_name}, {e}")
        return False

def get_assistant(asst_name):
    try:
        assistant = pc.assistant.describe_assistant(assistant_name=asst_name)
        while assistant.status == "Initializing":
            time.sleep(1)
        return assistant
    except Exception as e:
        print(f"Exception when describing assistant {asst_name}, error {e}")
        return False

def main():
    assistant = get_assistant(asst_name)
    if not assistant:
        print(f"Assistant {asst_name} doesn't exist")
        assistant = create_pinecone_assistant(asst_name)
    print(f"Getting list of blobs")
    blob_names = list_blobs_in_container()
    for blob_name in blob_names:
        print(f"Working on {blob_name}")
        file_path = download_blob(blob_name)
        upload_to_pinecone_assistant(assistant, file_path)
        os.remove(file_path)  # Clean up the downloaded file after upload

if __name__ == "__main__":
    main()