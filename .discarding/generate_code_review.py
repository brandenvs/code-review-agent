import psycopg2


def stream_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        raw_file = file.read()
        encoded_bytes = raw_file.encode('utf-8', errors='replace')
        query_text = encoded_bytes.decode('ascii', errors='replace')
    return query_text


def generate_code_review(db_config):
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        file_path = input('Enter path to code file:\n> ')
        code_content_1 = stream_code_file(file_path)

        file_path = input('Enter path to SECOND code file:\n> ')
        code_content_2 = stream_code_file(file_path)

        '''query_text_1 TEXT, query_text_2 TEXT, task_title TEXT, file_name TEXT'''
        print('Generating Code Review ')
        cursor.execute("SELECT generate_review(%s, %s, %s, %s);", (code_content_1, code_content_2, 'OOP – Classes', ''))
        generated_review = cursor.fetchone()[0]  # Fetch the generated review

        conn.commit()
        print(f"Generated Review: {generated_review}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    generate_code_review(db_config)
