import os
import sys

# Add the project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from file_manager import *
import os, time
import logging

def main():
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

if __name__ == '__main__':
    main()