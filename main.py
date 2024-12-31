from processors.task_processor import stream_task_pdf, insert_instructions
from processors.code_processor import stream_code_file, insert_code
from processors.review_processor import (
    stream_review, 
    split_review, 
    insert_review
)
import time


if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    pdf_path = "task_instructions/10-023 Programming with User-defined Functions.pdf"
    task_title, task_instructions = stream_task_pdf(pdf_path)

    code_path = "model_answers/latest_version_holiday.py"
    code = stream_code_file(code_path)

    review_path = "sample_reviews/sample_review1.txt"
    review_text = stream_review(review_path)
    segmented_review = split_review(review_text)

    task_instructions_id = insert_instructions(db_config, task_title, task_instructions)

    time.sleep(5)
    print('task_instructions_id' ,task_instructions_id)

    code_solution_id = insert_code(db_config, task_instructions_id, task_title, code)

    time.sleep(5)
    print('code_solution_id', code_solution_id)

    code_review_id = insert_review(db_config, code_solution_id, task_title, segmented_review)
