from azure.storage.blob import BlobServiceClient
from pinecone import Pinecone
import os

# Fetching environment variables
storage_account_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

def list_blobs_in_container():
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs()
    return [blob.name for blob in blob_list]

def download_blob(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    download_file_path = os.path.join(os.getcwd(), blob_name)
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    return download_file_path

def create_pinecone_assistant():
    metadata = {"author": "Cory Waddingham", "version": "0.1"}
    assistant = pc.assistant.create_assistant(
        assistant_name=os.getenv("PINECONE_ASSISTANT_NAME") or "example-assistant",
        metadata=metadata, 
        timeout=30  # Wait 30 seconds for assistant operation to complete.
    )
    return assistant

def upload_to_pinecone_assistant(assistant, file_path):
    response = assistant.upload_file(
        file_path=file_path,
        timeout=None
    )

    if response.status_code == 200:
        print(f"File {file_path} uploaded successfully to Pinecone Assistant.")
    else:
        print(f"Failed to upload {file_path}. Status code: {response.status_code}, Response: {response.text}")

def main():
    assistant = create_pinecone_assistant()
    if not assistant:
        raise Exception("Assistant creation failed")

    blob_names = list_blobs_in_container()

    for blob_name in blob_names:
        file_path = download_blob(blob_name)
        upload_to_pinecone_assistant(assistant, file_path)
        os.remove(file_path)  # Clean up the downloaded file after upload

if __name__ == "__main__":
    main()
