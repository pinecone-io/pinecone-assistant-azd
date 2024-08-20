from file_manager import *
import os, time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
import os

def get_files_to_process(directory, processed_files_path):
    all_files = [f for f in os.listdir(directory) if f.endswith('.pdf') or f.endswith('.txt')]
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as file:
            processed_files = file.read().splitlines()
    else:
        processed_files = []
    return [f for f in all_files if f not in processed_files]

def main():
    assistant = get_assistant(asst_name)
    if not assistant:
        print(f"Assistant {asst_name} doesn't exist")
        assistant = create_pinecone_assistant(asst_name)
    
    assets_directory = os.path.join(os.getcwd(), "assets")
    processed_files_path = os.path.join(assets_directory, "processed_files")
    
    files_to_process = get_files_to_process(assets_directory, processed_files_path)
    
    logger.info(f"Getting list of files")
    for file_name in files_to_process:
        file_path = os.path.join(assets_directory, file_name)
        print(f"Working on {file_name}")
        upload_to_pinecone_assistant(assistant, file_path)
        with open(processed_files_path, 'a') as file:
            file.write(file_name + '\n')

if __name__ == "__main__":
    main()