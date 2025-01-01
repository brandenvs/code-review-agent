import psycopg2


def stream_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        parsed_code = file.read()
    return parsed_code


def generate_code_review(db_config):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        file_path = input('Enter path to code file:\n> ')
        student_name = input('Enter student name:\n> ')
        task_title = input('Enter task title:\n> ')

        code_content = stream_code_file(file_path)

        print('Generating Code Review ')
        # Call the `generate_code_review` function
        cursor.execute("SELECT generate_code_review(%s, %s, %s);", (code_content, student_name, task_title,))
        generated_review = cursor.fetchone()[0]  # Fetch the generated review

        conn.commit()
        print(f"Generated Review: {generated_review}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()


# Example usage
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    generate_code_review(db_config)
