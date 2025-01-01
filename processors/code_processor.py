import psycopg2
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def stream_code_file(file_path):
    with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8', errors='replace') as file:
        parsed_code = file.read()
    return parsed_code


def insert_code(db_config, task_instructions_id, task_title, code):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO code_solutions (task_instructions_id, title, code)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        cursor.execute(insert_query, (task_instructions_id, task_title, code))

        conn.commit()

        inserted_id = cursor.fetchone()[0]

        print(f"Code solution for '{task_title}' successfully inserted into table!.")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()
