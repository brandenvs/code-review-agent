from processors.task_processor import extract_pdf_content, save_structured_content
from processors.code_processor import stream_code_file, insert_code
from processors.review_processor import (
    stream_review, 
    split_review, 
    insert_review
)
import argparse
from pathlib import Path
import os

import psycopg2

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
                break

    except Exception as e:
        print(f"An error occurred while searching the directory: {e}")
    return found_files


def insert_instructions(db_config, task_title, task_instructions):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO task_instructions (title, compulsory_task_1, compulsory_task_2)
        VALUES (%s, %s, NULL)
        RETURNING id;
        """


        cursor.execute(insert_query, (task_title, task_instructions))
        conn.commit()

        inserted_id = cursor.fetchone()[0]
        

        print(f"Task instructions for '{task_title}' successfully inserted into table!.")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    dirs = list_folders('data')

    parser = argparse.ArgumentParser(description="Find PDF documents and Python scripts in a directory.")
    parser.add_argument("-d", "--directory", default=".", help="The directory to search in. Defaults to current directory.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search recursively through subdirectories.")
    args = parser.parse_args()

    task_pdfs = []
    reviews = []

    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    for directory in dirs:
        search_dir = f'data/{directory}'
        student_dirs = list_folders(search_dir)

        for student_dir in student_dirs:
            student_path = f'{search_dir}/{student_dir}'
            extensions = ('.pdf', '.py', '.txt')

            found_files = find_files(student_path, extensions, True)

            task_title = None
            task_instructions = None
            code = None
            segmented_review = None

            for file in found_files:
                if file.endswith('.pdf'):
                    if len(file.split('\\')) <= 4:  # Only consider files at the root level for the student
                        output_path = f'{file}.json'
                        structured_content = extract_pdf_content(file)

                        task_pdfs.append(structured_content)

                        # Extract task title and instructions
                        task_title = structured_content[0]['content']
                        for obj in structured_content:
                            if obj['section'] == 'Instructions':
                                task_instructions = obj['content']

                        save_structured_content(structured_content, output_path)

                elif file.endswith('.py'):
                    if len(file.split('\\')) <= 4:
                        code = stream_code_file(file)

                elif file.endswith('.txt'):
                    if len(file.split('\\')) <= 4:
                        review_text = stream_review(file)
                        segmented_review = split_review(review_text)

            # Insert into the database for this student if necessary data is available
            if task_title and task_instructions:
                task_instructions_id = insert_instructions(db_config, task_title, task_instructions)

                if code:
                    code_solution_id = insert_code(db_config, task_instructions_id, task_title, code)

                    if segmented_review:
                        code_review_id = insert_review(db_config, code_solution_id, task_title, segmented_review)


'''Initial Solution

if __name__ == "__main__":
    dirs = list_folders('data')

    parser = argparse.ArgumentParser(description="Find PDF documents and Python scripts in a directory.")
    parser.add_argument("-d", "--directory", default=".", help="The directory to search in. Defaults to current directory.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search recursively through subdirectories.")
    args = parser.parse_args()

    task_pdfs = []
    reviews = []

    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    for directory in dirs:
    search_dir = f'data/{directory}'
    extensions = ('.pdf', '.py', '.txt')

    found_files = find_files(search_dir, extensions, True)

    for i, file in enumerate(found_files):
        if file.endswith('.pdf'):
            if len(file.split('\\')) <= 3:
                output_path = f'{file}.json'
                structured_content = extract_pdf_content(file)
            
                task_pdfs.append(structured_content)

                task_title = structured_content[0]['content']

                for i, obj in enumerate(structured_content):
                    if obj['section'] == 'Instructions':
                        task_instructions = structured_content[i]['content']

                save_structured_content(structured_content, output_path)
        
        elif file.endswith('.py'):
            if len(file.split('\\')) <= 3:
                print(file)
                code = stream_code_file(file)
        
        elif file.endswith('.txt'):
            review_text = stream_review(file)
            segmented_review = split_review(review_text)

    task_instructions_id = insert_instructions(db_config, task_title, task_instructions)
    code_solution_id = insert_code(db_config, task_instructions_id, task_title, code)
    code_review_id = insert_review(db_config, code_solution_id, task_title, segmented_review)
'''
