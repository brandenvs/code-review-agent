'''SCHEMA
code_reviews (
    id SERIAL PRIMARY KEY,
    review_sentiment TEXT,
    review_text TEXT NOT NULL
);
'''
import psycopg2


db_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}


def insert_review(review_sentiment, review_text):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO code_reviews (review_sentiment, review_text)
        VALUES (%s, %s)
        RETURNING id;
        """

        cursor.execute(
            insert_query,
            (
                review_sentiment,
                review_text,
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

        cursor.execute(insert_query, (review_id, file_name, file_content))

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