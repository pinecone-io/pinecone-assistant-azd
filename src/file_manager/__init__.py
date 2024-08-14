from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm
import os, time

# Fetching environment variables
load_dotenv('.env.azure', override=True)
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group_name = os.getenv("AZURE_RESOURCE_GROUP")
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
asst_name = os.getenv("PINECONE_ASSISTANT_NAME")

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

def get_storage_account_connection_string(subscription_id, resource_group_name, storage_account_name):
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)
    keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
    account_key = keys.keys[0].value
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return connection_string
# Fetch the connection string
storage_account_connection_string = get_storage_account_connection_string(subscription_id, resource_group_name, storage_account_name)