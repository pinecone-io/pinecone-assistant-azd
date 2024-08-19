from azure import functions as func
from pinecone import Pinecone
from file_manager import *
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_processed_files(container_client):
    try:
        blob_client = container_client.get_blob_client("processed_files")
        download_stream = blob_client.download_blob()
        processed_files = set(download_stream.content_as_text().splitlines())
    except Exception as e:
        print(f"Error loading processed files: {e}")
        processed_files = set()
    return processed_files

def save_processed_files(container_client, processed_files):
    try:
        blob_client = container_client.get_blob_client("processed_files")
        blob_client.upload_blob("\n".join(processed_files), overwrite=True)
    except Exception as e:
        if "BlobNotFound" in str(e):
            blob_client.upload_blob("\n".join(processed_files))
        else:
            print(f"Error saving processed files: {e}")

def poll_blob_storage():
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    existing_blobs = load_processed_files(container_client)

    pc = Pinecone(api_key=pinecone_api_key)
    assistant = pc.assistant.Assistant(assistant_name=asst_name)

    current_blobs = {blob.name for blob in container_client.list_blobs() if (blob.name.endswith(".pdf") or blob.name.endswith(".txt"))}
    new_blobs = current_blobs - existing_blobs
    deleted_blobs = existing_blobs - current_blobs

    if not new_blobs and not deleted_blobs:
        print(f"No files to process.")
        return

    for blob_name in new_blobs:
        print(f"New blob detected: {blob_name}")
        file_path = download_blob(blob_name)
        upload_to_pinecone_assistant(assistant, file_path)
        os.remove(file_path)
        existing_blobs.add(blob_name)

    for blob_name in deleted_blobs:
        print(f"Deleted blob detected: {blob_name}")
        files = assistant.list_files()
        file_id = next((file.id for file in files if file.name == blob_name), None)

        if file_id:
            assistant.delete_file(file_id=file_id)
            print(f"File {blob_name} deleted from assistant.")
            existing_blobs.remove(blob_name)
        else:
            print(f"File {blob_name} not found in assistant.")

    save_processed_files(container_client, existing_blobs)

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Timer trigger function executed at %s', mytimer.schedule_status.last)
    poll_blob_storage()

if __name__ == "__main__":
    main()