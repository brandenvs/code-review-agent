'''SCHEMA
code_reviews (
    id SERIAL PRIMARY KEY,
    review_sentiment TEXT,
    review_text TEXT NOT NULL
);

solution_files (
    id SERIAL PRIMARY KEY,
    review_id INT NOT NULL,
    file_name TEXT NOT NULL,
    file_content  TEXT NOT NULL,
    FOREIGN KEY (review_id) REFERENCES code_reviews (id) ON DELETE CASCADE
);

task_instructions (
    id SERIAL PRIMARY KEY,
    solution_id INT NOT NULL,
    task_name TEXT NOT NULL,
    task_content TEXT NOT NULL,
    task_instructions TEXT NOT NULL,
    FOREIGN KEY (solution_id) REFERENCES solution_files (id) ON DELETE CASCADE
);
'''
import psycopg2
import json


db_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

def insert_task(task_name, task_content, task_instructions):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO tasks (task_name, task_content, task_instructions)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        cursor.execute(
            insert_query, (task_name, task_content, task_instructions)
        )

        inserted_id = cursor.fetchone()[0]
        conn.commit()

        print(f"ADDED Code Review!\n\tID: {inserted_id}")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_model_answer(task_id, task_name, file_content, metadata={}):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO model_answers (task_id, task_name, file_content, metadata)
        VALUES (%s, %s, %s, %s::jsonb)
        RETURNING id;
        """
        metadata_json = json.dumps(metadata)

        cursor.execute(
            insert_query, 
            (
                task_id,
                task_name,
                file_content, 
                metadata_json 
            )
        )

        conn.commit()

        inserted_id = cursor.fetchone()[0]

        print(f"ADDED Model Answer for {task_id}!\n\tID: {inserted_id}")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_review(task_name, review_average_sentiment, review_text, metadata):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        metadata_json = json.dumps(metadata)

        # Normalize the task_name to lowercase
        task_name = task_name.lower()

        # SQL query to find task ID
        select_query = """
        SELECT id FROM tasks
        WHERE task_name ILIKE %s;
        """

        cursor.execute(select_query, (task_name,))
        task_id = cursor.fetchone()

        # Handle the result of the query
        if task_id:
            print(f"Task ID: {task_id[0]}")
        else:
            print("Task not found")
            return None

        insert_query = """
        INSERT INTO code_reviews (task_id, review_average_sentiment, review_text, metadata)
        VALUES (%s, %s, %s, %s::jsonb)
        RETURNING id;
        """

        cursor.execute(
            insert_query,
            (
                task_id,
                review_average_sentiment,
                review_text,
                metadata_json
            )
        )

        inserted_id = cursor.fetchone()[0]
        conn.commit()

        print(f"ADDED Code Review!\n\tID: {inserted_id}")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_solution(review_id, file_name, file_content):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO solution_files (review_id, file_name, file_content)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        cursor.execute(
            insert_query, 
            (
                review_id, 
                file_name, 
                file_content
            )
        )

        conn.commit()

        inserted_id = cursor.fetchone()[0]

        print(f"ADDED Code Solution!\n\tID: {inserted_id}\n\tReview ID: {review_id}")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_task(task_name, task_content, task_instructions):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO tasks (task_name, task_content, task_instructions)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        cursor.execute(
            insert_query, 
            (
                task_name, 
                task_content, 
                task_instructions
            )
        )

        conn.commit()

        inserted_id = cursor.fetchone()[0]

        print(f"ADDED Task!\n\tID: {inserted_id}")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()
