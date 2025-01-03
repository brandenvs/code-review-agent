import psycopg2
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def stream_code_file(file_path):
    with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8', errors='replace') as file:
        parsed_code = file.read()
    return parsed_code


def insert_solution(db_config, review_id, file_name, file_content):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO code_solutions (review_id, file_name, file_content)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        cursor.execute(insert_query, (review_id, file_name, file_content))

        conn.commit()

        inserted_id = cursor.fetchone()[0]

        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()
