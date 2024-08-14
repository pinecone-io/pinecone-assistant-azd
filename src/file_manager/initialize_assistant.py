from azure.storage.blob import BlobServiceClient
from . import *
import os, time


def list_blobs_in_container():
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    return [blob.name for blob in blob_list]

def get_blob_line_count(blob_client):
    download_stream = blob_client.download_blob()
    line_count = sum(1 for _ in download_stream.chunks())
    return line_count

def download_blob(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    download_file_path = os.path.join(os.getcwd(), "tmp", blob_name)
    line_count = get_blob_line_count(blob_client)
    with open(download_file_path, "wb") as download_file:
        download_stream = blob_client.download_blob()
        for chunk in tqdm(download_stream.chunks(), total=line_count, desc=f"Downloading {blob_name}"):
            download_file.write(chunk)
    download_file_path = os.path.join(os.getcwd(), blob_name)
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    return download_file_path

def upload_blob(file_path):
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(os.path.basename(file_path))
    with open(file_path, "rb") as data:
        total_size = os.path.getsize(file_path)
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Uploading {os.path.basename(file_path)}") as pbar:
            blob_client.upload_blob(data, raw_response_hook=lambda response: pbar.update(len(response.http_response.body())))
    print(f"File {file_path} uploaded to blob storage.")

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

def upload_to_pinecone_assistant(assistant, file_path):
    response = assistant.upload_file(
        file_path=file_path,
        timeout=None
    )
    if response.status == "Available":
        print(f"File {file_path} uploaded successfully to Pinecone Assistant.")
    else:
        print(f"Failed to upload {file_path}. Status code: {response.status}, Response: {response.error}")

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