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