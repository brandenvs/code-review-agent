from pathlib import Path
import os

import spacy
from spacy.tokens import Span
from textblob import TextBlob
import re

BASE_DIR = Path(__file__).resolve().parent.parent

if not Span.has_extension("sentiment"):
    Span.set_extension("sentiment", default=None)


def stream_review(file_path):
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
        task_name_pattern = r"^Task name:\s*(.+)$"
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

        review_text = no_noise.split('Positive')[1]

        # Remove headers or specific lines
        processed_review = re.sub(r'(-{3,}|={3,}|Review ID:.*)', '', review_text)

        # Normalises whitespace
        processed_review = ' '.join(processed_review.split())
        print(processed_review)

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

    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    #     return None


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