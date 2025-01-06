from pathlib import Path
import os
import re

import spacy
from spacy.tokens import Span
from textblob import TextBlob

from db_processing.db_inserts import insert_review


BASE_DIR = Path(__file__).resolve().parent.parent

if not Span.has_extension("sentiment"):
    Span.set_extension("sentiment", default=None)


def sentiment_review(process_review):
    for sent in process_review.sents:
        blob = TextBlob(sent.text)
        # Normalize polarity to range [0, 1]
        normalized_sentiment = (blob.sentiment.polarity + 1) / 2
        sent._.sentiment = normalized_sentiment
    return process_review


@spacy.language.Language.component("sentiment_review")
def sentiment_component(process_review):
    return sentiment_review(process_review)

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
    # spaCy setup
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("sentiment_review", last=True)

    try:
        full_path = os.path.join(BASE_DIR, file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {full_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            raw_review_text = file.read()
            encoded_bytes = raw_review_text.encode('utf-8', errors='ignore')
            no_noise = encoded_bytes.decode('ascii', errors='ignore')

        # Regular expressions
        student_pattern = r"^Student:\s*(.+)$"
        task_name_pattern = r"^Task name: Task \d+ - (.+)"
        course_pattern = r"^Course:\s*(.+)$"

        # Extracting the values using re.search with multiline support
        student_match = re.search(student_pattern, raw_review_text, re.MULTILINE)
        task_name_match = re.search(task_name_pattern, raw_review_text, re.MULTILINE)
        course_match = re.search(course_pattern, raw_review_text, re.MULTILINE)

        # Extract values safely
        student = student_match.group(1).strip() if student_match else None
        task_name = task_name_match.group(1).strip() if task_name_match else None
        course = course_match.group(1).strip() if course_match else None

        # Check for missing matches
        if not all([student, task_name, course]):
            raise ValueError("Failed to extract some required fields from the review.")

        # task_name = task_name.split(' - ')
        # task_name.pop(0)

        # task_name = ''.join(task_name).strip()
        review_text = no_noise.split('Positive')[1]

        # Remove headers or specific lines
        processed_review = re.sub(r'(-{3,}|={3,}|Review ID:.*)', '', review_text)

        # Normalises whitespace
        processed_review = ' '.join(processed_review.split())

        meta_data = {
            'metadata': [
                {
                    'student': student,
                    'course': course
                }
            ],
        }

        review_analysis = nlp(review_text)

        review_sentiment = [sent._.sentiment for sent in review_analysis.sents]

        # Calculate mean avg
        review_average_sentiment = sum(review_sentiment) / len(review_sentiment) if review_sentiment else 0
        
        insert_review(task_name, review_average_sentiment, review_text, meta_data)

        review_content = {
            'metadata': [
                {
                    'student': student,
                    'course': course
                }
            ],
            'title': task_name,
            'review_text': processed_review
        }
        return review_content

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        return None

if __name__ == "__main__":
    dirs = list_folders('data')

    final_search_dirs = []

    get_file_name = lambda x: Path(x).name

    for student_dir in dirs:
        search_dir = f'data/{student_dir}'
        student_tasks_dirs = list_folders(search_dir)

        for task_dir in student_tasks_dirs:
            final_search_dirs.append(f'data/{student_dir}/{task_dir}')
    
    for final_dir in final_search_dirs:
        dir_files = find_files(final_dir, '.txt')
        for dir_file in dir_files:
            file_name = get_file_name(dir_file)
            if file_name == 'review_text.txt':
                processor(dir_file)

        
    #     task_dirs.append(list_folders(search_dir))

    # for task in task_dirs:
    #     task_dir = f'data/{student_dir}/{task[0]}'
    #     print(task_dir)
    #     task_files = find_files(task_dir, '.txt')

    #     for file_path in task_files:
    #         file_name = get_file_name(file_path)
    #         file_name

    #         if file_name == 'review_text.txt':
    #             print(file_path)
    #             # processor(file_path)





