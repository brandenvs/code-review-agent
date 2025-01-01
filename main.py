from processors.task_processor import insert_instructions, save_structured_content_for_pgai, process_pdf_for_pgai
from processors.code_processor import stream_code_file, insert_code
from processors.review_processor import (
    stream_review, 
    split_review, 
    insert_review
)
import time
import argparse
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
def list_folders(directory, recursive=False, indent=""):
    dirs = []
    try:
        abs_directory = os.path.abspath(directory)
        
        items = os.listdir(abs_directory)
        
        folders = [item for item in items if os.path.isdir(os.path.join(abs_directory, item))]
        
        # Print the folders
        for folder in folders:
            print(f"{indent}{folder}")
            dirs.append(folder)
            
            if recursive:
                subfolder_path = os.path.join(abs_directory, folder)
                list_folders(subfolder_path, recursive, indent + "  ")
    
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return dirs


def find_files(directory, extensions, recursive=False):
    found_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    found_files.append(os.path.join(root, file))
            if not recursive:
                break  # Stop after the first iteration if not recursive
    except Exception as e:
        print(f"An error occurred while searching the directory: {e}")
    return found_files


if __name__ == "__main__":
    dirs = list_folders('data')

    parser = argparse.ArgumentParser(description="Find PDF documents and Python scripts in a directory.")
    parser.add_argument("-d", "--directory", default=".", help="The directory to search in. Defaults to current directory.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search recursively through subdirectories.")
    args = parser.parse_args()

    for directory in dirs:
        search_dir = f'data/{directory}'
        extensions = ('.pdf', '.py')

        found_files = find_files(search_dir, extensions, True)

        for i, file in enumerate(found_files):
            if file.endswith('.pdf'):
                output_path = f'{file}.json'
                process_pdf_for_pgai(file, output_path)

    # db_config = {
    #     'host': 'localhost',
    #     'database': 'postgres',
    #     'user': 'postgres',
    #     'password': 'postgres'
    # }

    # pdf_path = "task_instructions/10-023 Programming with User-defined Functions.pdf"
    # task_title, task_instructions = stream_task_pdf(pdf_path)

    # code_path = "model_answers/latest_version_holiday.py"
    # code = stream_code_file(code_path)

    # review_path = "sample_reviews/sample_review1.txt"
    # review_text = stream_review(review_path)
    # segmented_review = split_review(review_text)

    # task_instructions_id = insert_instructions(db_config, task_title, task_instructions)

    # time.sleep(5)
    # print('task_instructions_id' ,task_instructions_id)

    # code_solution_id = insert_code(db_config, task_instructions_id, task_title, code)

    # time.sleep(5)
    # print('code_solution_id', code_solution_id)

    # code_review_id = insert_review(db_config, code_solution_id, task_title, segmented_review)
