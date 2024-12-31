import psycopg2
import fitz  # PyMuPDF
import re
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def stream_task_pdf(file_path):
    pdf_document = fitz.open(os.path.join(BASE_DIR, file_path))

    text = ""

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    match_task_instructions = re.search(r"Compulsory Task 1(.*?)Hyperion strives to provide", text, re.DOTALL)
    match_task_title = re.search(r"TASK(.*?)Introduction", text, re.DOTALL)

    task_title = match_task_title.group(1).strip()
    task_instructions = match_task_instructions.group(1).strip()

    return task_title, task_instructions


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
