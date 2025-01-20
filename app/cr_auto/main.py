from pathlib import Path
import os


import psycopg2
import json

BASE_DIR = Path(__file__).resolve().parent.parent


def list_folders(directory, recursive=False, indent=""):
    dirs = []

    try:
        abs_directory = os.path.abspath(directory)

        items = os.listdir(abs_directory)

        folders = [item for item in items if os.path.isdir(os.path.join(abs_directory, item))]

        # Print the folders
        for folder in folders:
            # print(f"{indent}{folder}")
            dirs.append(folder)

            if recursive:
                subfolder_path = os.path.join(abs_directory, folder)
                list_folders(subfolder_path, recursive, indent + "  ")

    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")

    except PermissionError:
        print(f"Error: Permission denied to access '{directory}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

    return dirs

db_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

def insert_task(
    task_name, task_content, task_instructions, 
    task_model_answer, task_model_answer1, 
    metadata={}):
    '''
    id SERIAL PRIMARY KEY,
    task_name TEXT NOT NULL,
    task_content TEXT NOT NULL,
    task_instructions TEXT NOT NULL,
    model_answer TEXT NOT NULL,
    metadata JSONB
    '''
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO tasks (task_name, task_content, task_instructions, model_answer_1, model_answer_2, metadata)
        VALUES (%s, %s, %s, %s, %s, %s::jsonb)
        RETURNING id;
        """

        metadata_json = json.dumps(metadata)

        cursor.execute(
            insert_query, (
                task_name, 
                task_content, 
                task_instructions,
                task_model_answer,
                task_model_answer1,
                metadata_json
            )
        )

        task_id = cursor.fetchone()[0]
        conn.commit()

        print(f"ADDED Task!\n\tID: {task_id}")
        return task_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_review(
    task_id, task_name, review_content, 
    submitted_content_1, submitted_content_2, 
    metadata={}):
    '''
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL,
    review_content TEXT NOT NULL,
    submitted_content_1 TEXT NOT NULL,
    submitted_content_2 TEXT NOT NULL,
    metadata JSONB,
    '''
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO reviews (task_id, task_name, review_content, submitted_content_1, submitted_content_2, metadata)
        VALUES (%s, %s, %s, %s, %s, %s::jsonb)
        """

        metadata_json = json.dumps(metadata)

        cursor.execute(
            insert_query, (
                task_id,
                task_name,
                review_content, 
                submitted_content_1,
                submitted_content_2,
                metadata_json
            )
        )

        conn.commit()

        print(f"ADDED Code Review!\n\tID: {task_id}")
        return task_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def review_processor(task_id, task_name, review_dir, options=None):
    review_content_file = f'{review_dir}/review_text.txt'
    review_submission_file = f'{review_dir}/submission.py'
    review_submission_file1 = f'{review_dir}/submission1.py'

    print('Now processing review for directory: ', review_dir)

    # Gets review text and processes
    with open(review_content_file,  "r", encoding="utf-8", errors='ignore') as file:
        raw_file = file.read()
        encoded_bytes = raw_file.encode('utf-8', errors='ignore')
        dirty_review_content = encoded_bytes.decode('ascii', errors='ignore')

        # Cleans the text
        dirty_review_content = dirty_review_content.split('Positive').pop(0)
        review_content = "\n".join(dirty_review_content)

        print('Original:')
        print(review_content)

        while True:
            print('Preprocessing extension - Select your schema:')
            print('0 - Default')
            print('1 - Lowercase/uppercase normalisation')
            print('2 - Remove noise')
            print('3 - Normalisation and remove noise')

            match options:
                case 0:
                    print('Applying `default` schema ...')
                    # TODO Default
                    break

                case 1:
                    print('Applying `normalisation` schema ...')
                    # TODO Lowercase/uppercase normalisation
                    break

                case 2:
                    print('Removing Noise and applying `default` schema ...')
                    # TODO Remove noise
                    break

                case 3:
                    print('Removing Noise and applying `normalisation` schema ...')
                    # TODO Normalisation and remove noise
                    break

                case _:
                    print('Invalid option, try again!')
                    continue


    # Gets and processed code submission
    with open(review_submission_file, "r", encoding="utf-8", errors='ignore') as file:
        raw_file = file.read()
        encoded_bytes = raw_file.encode('utf-8', errors='ignore')
        review_submission_1 = encoded_bytes.decode('ascii', errors='ignore')

    # Gets and processes 2nd code submission
    if os.path.exists(review_submission_file1):
        with open(review_submission_file1, 'r', encoding='utf-8') as file:
            raw_file = file.read()
            encoded_bytes = raw_file.encode('utf-8', errors='ignore')
            review_submission_2 = encoded_bytes.decode('ascii', errors='ignore')

    else:
        review_submission_2 = 'There is only one submission file'

    # Create review records
    insert_review(
        task_id,
        task_name,
        review_content,
        review_submission_1,
        review_submission_2
    )


def task_processor(task_dir):
    task_name_file = f'{task_dir}/task_name.txt'
    task_content_file = f'{task_dir}/task_content.txt'
    task_instructions_file = f'{task_dir}/task_instructions.txt'

    task_model_answer_file = f'{task_dir}/model_answer/model_answer.py'
    task_model_answer_file1 = f'{task_dir}/model_answer/model_answer1.py'


    with open(task_name_file,  "r", encoding="utf-8") as file:
        task_name = file.readline()
        task_name = task_name.replace('\ufeff', '')


    with open(task_content_file, "r", encoding="utf-8") as file:
        raw_file = file.read()
        encoded_bytes = raw_file.encode('utf-8', errors='ignore')
        task_content = encoded_bytes.decode('ascii', errors='ignore')


    with open(task_instructions_file, "r", encoding="utf-8") as file:
        raw_file = file.read()
        encoded_bytes = raw_file.encode('utf-8', errors='ignore')
        task_instructions = encoded_bytes.decode('ascii', errors='ignore')


    with open(task_model_answer_file, 'r', encoding='utf-8') as file:
        raw_file = file.read()
        encoded_bytes = raw_file.encode('utf-8', errors='ignore')
        task_model_answer = encoded_bytes.decode('ascii', errors='ignore')

    if os.path.exists(task_model_answer_file1):
        with open(task_model_answer_file1, 'r', encoding='utf-8') as file:
            raw_file = file.read()
            encoded_bytes = raw_file.encode('utf-8', errors='ignore')
            task_model_answer1 = encoded_bytes.decode('ascii', errors='ignore')

    else:
        task_model_answer1 = 'There is only one model answer for this task'

    task_id = insert_task(
        task_name, 
        task_content, 
        task_instructions, 
        task_model_answer,
        task_model_answer1
    )
    return task_id, task_name


if __name__ == "__main__":
    base_dir = BASE_DIR / 'cr_auto/data'
    folders = list_folders(base_dir)

    get_file_name = lambda x: Path(x)

    for folder in folders:
        task_id, task_name = task_processor(f'{base_dir}/{folder}')

        submission_folders = list_folders(f'{base_dir}/{folder}/reviews/')
        for _folder in submission_folders:
            review_processor(task_id, task_name, f'{base_dir}/{folder}/reviews/{_folder}')
