from opencensus.ext.azure.log_exporter import AzureLogHandler
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm
import os, time
import logging

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=<your_instrumentation_key>'))

# Fetching environment variables
load_dotenv('.env.azure', override=True)
key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group_name = os.getenv("AZURE_RESOURCE_GROUP")
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
asst_name = os.getenv("PINECONE_ASSISTANT_NAME")

# Initialize the Key Vault client
try:
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    # Fetch the Instrumentation Key from Key Vault
    instrumentation_key = client.get_secret("InstrumentationKey").value
except Exception as e:
    print(f"Something went wrong getting the key vault, error was {e}")
    logger.error(f"Something went wrong getting the key vault, error was {e}")
    exit(1)

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

def get_blob_line_count(blob_client):
    download_stream = blob_client.download_blob()
    line_count = sum(1 for _ in download_stream.chunks())
    return line_count

def get_storage_account_connection_string(subscription_id, resource_group_name, storage_account_name):
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)
    keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
    account_key = keys.keys[0].value
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return connection_string
# Fetch the connection string
storage_account_connection_string = get_storage_account_connection_string(subscription_id, resource_group_name, storage_account_name)

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

def upload_to_pinecone_assistant(assistant, file_path):
    if file_path.endswith(".pdf") or file_path.endswith(".txt"):
        response = assistant.upload_file(
            file_path=file_path,
            timeout=None
        )
        if response.status == "Available":
            logger.info(f"File {file_path} uploaded successfully to Pinecone Assistant.")
        else:
            logger.error(f"Failed to upload {file_path}. Status code: {response.status}, Response: {response.error}")
    else:
        logger.error(f"Invalid file type, skipping {file_path}.")
