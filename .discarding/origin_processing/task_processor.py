from pathlib import Path
import os
import re
from db_processing.db_inserts import insert_task

BASE_DIR = Path(__file__).resolve().parent.parent

def list_folders(directory, recursive=False, indent=""):
    dirs = []

    try:
        abs_directory = os.path.abspath(directory)

        items = os.listdir(abs_directory)

        folders = [item for item in items if os.path.isdir(os.path.join(abs_directory, item))]

        # Print the folders
        for folder in folders:
            # print(f"{indent}{folder}")
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


def find_files(directory, extensions, recursive=False) -> list[str]:
    found_files = []

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    found_files.append(os.path.join(root, file))

            if not recursive:
                break

    except Exception as e:
        print(f"An error occurred while searching the directory: {e}")
    return found_files

def processor(file_path):
    result = {}

    try:
        full_path = os.path.join(BASE_DIR, file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {full_path}")
    
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline()
            raw_file = file.read()
            encoded_bytes = raw_file.encode('utf-8', errors='ignore')
            no_noise = encoded_bytes.decode('ascii', errors='ignore')

        segmented_pdf = no_noise.split('Instructions')

        if len(segmented_pdf) < 2:
            segmented_pdf = no_noise.split('Practical task')
        
        if len(segmented_pdf) < 2:
            segmented_pdf = no_noise.split('Auto-graded task')
        
        if len(segmented_pdf) < 2:
            segmented_pdf = no_noise.split('Practical Task')
        
        if len(segmented_pdf) == 3:
            segmented_pdf = segmented_pdf[1].join(segmented_pdf[2])

        task_content = no_noise[0].strip()

        task_instructions = segmented_pdf[1]
        task_instructions = task_instructions.split('Share your thoughts')[0].strip()

        task_name = first_line.replace('\ufeff', '').strip('\n').lower()

        insert_task(task_name, task_content, task_instructions)

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        return None


if __name__ == "__main__":
    files = find_files('task_data', '.txt')

    for file in files:
        print(file)
        processor(file)