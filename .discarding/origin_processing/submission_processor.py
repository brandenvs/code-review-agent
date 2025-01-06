import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def read_submission_file(file_path):
    with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8', errors='replace') as file:
        submission_text = file.read()
    return submission_text
