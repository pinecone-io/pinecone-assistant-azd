from opencensus.ext.azure.log_exporter import AzureLogHandler
from azure.identity import DefaultAzureCredential
from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone.core.client.exceptions import UnauthorizedException
from tqdm import tqdm
import os, sys, time
import logging

from azure.identity import DefaultAzureCredential

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Fetching environment variables
load_dotenv('.env.azure', override=True)
pinecone_api_key = os.getenv("PINECONE_API_KEY")
asst_name = os.getenv("PINECONE_ASSISTANT_NAME")
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group_name = os.getenv("AZURE_RESOURCE_GROUP")
app_insights_name = os.getenv("APP_INSIGHTS_NAME")


credential = DefaultAzureCredential()
client = ApplicationInsightsManagementClient(credential, subscription_id)
app_insights = client.components.get(resource_group_name, app_insights_name)
instrumentation_key = app_insights.instrumentation_key

logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={instrumentation_key}'))


# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)
# Check that the API key is valid
try:
    indexes = pc.list_indexes()
except UnauthorizedException as e:
    print(f'The API key "{pinecone_api_key}" is not valid, please be sure to use a valid Pinecone API key.')
    print(f"Use https://app.pinecone.io/organizations/-/projects/-/keys to create or fetch a key.")
    sys.exit(1)

def get_files_to_process(directory, processed_files_path):
    all_files = [f for f in os.listdir(directory) if f.endswith('.pdf') or f.endswith('.txt')]
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as file:
            processed_files = file.read().splitlines()
    else:
        processed_files = []
    return [f for f in all_files if f not in processed_files]

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

def get_assistant(asst_name):
    try:
        assistant = pc.assistant.describe_assistant(assistant_name=asst_name)
        while assistant.status == "Initializing":
            time.sleep(1)
        return assistant
    except Exception as e:
        print(f"Exception when describing assistant {asst_name}, error {e}")
        return False
import os