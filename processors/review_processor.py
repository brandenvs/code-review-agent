import psycopg2
import re
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def stream_review(file_path):
    with open(os.path.join(BASE_DIR, file_path), "r", encoding="utf-8") as file:
        review_text = file.read()

    # Clean and process the review text
    lines = review_text.split('\n')
    lines_cleaned = [
        line.strip().replace("=", "") for line in lines if len(line.strip()) > 0
    ]

    # Construct and return processed review str
    review_text = " ".join(lines_cleaned)
    return review_text

def split_review_old(processed_review_text):
    keywords = ["Positive", "Improve", "Overall"]

    # Regex pattern
    pattern = r'\b(' + '|'.join(keywords) + r')\b'

    split_text = re.split(pattern, processed_review_text)

    result = []
    for i in range(1, len(split_text), 2):
        result.append(split_text[i] + split_text[i + 1].strip())
    return result


def split_review(processed_review_text):
    keywords = ["Positive", "Improve", "Overall"]

    score_pattern = r'(Efficiency|Completeness|Style|Documentation):\s*([\d.]+)'

    scores = {match[0]: float(match[1]) for match in re.findall(score_pattern, processed_review_text)}

    # Regex pattern to split the text by keywords
    split_pattern = r'\b(' + '|'.join(keywords) + r')\b'
    split_text = re.split(split_pattern, processed_review_text)

    result = []
    for i in range(1, len(split_text), 2):
        result.append(split_text[i] + " " + split_text[i + 1].strip())

    # Add scores to the result
    result.append({"Scores": scores})
    print(result)

    return result


def insert_review(db_config, code_solution_id, task_title, segmented_review):
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
        INSERT INTO code_reviews (code_solution_id, title, review_positives, review_improvements, review_overall, score_completeness, score_efficiency, score_style, score_documentation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        scores = dict(segmented_review[-1])
        print(scores)

        scores_dict = dict(scores['Scores'])
        print(scores_dict)
        
        cursor.execute(
            insert_query,
            (
                code_solution_id,
                task_title,
                str(segmented_review[0]), # Positive
                str(segmented_review[1]), # Improve
                str(segmented_review[2]), # Overall
                int(scores_dict['Efficiency']),
                int(scores_dict['Completeness']),
                int(scores_dict['Documentation']),
                int(scores_dict['Style']),
            )
        )

        inserted_id = cursor.fetchone()[0]
        conn.commit()

        print(f"Task review for '{task_title}' successfully inserted into table!.")
        return inserted_id

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def split_review_with_metadata(processed_review_text):
    # Keywords to split the review
    keywords = ["Positive", "Improve", "Overall"]

    # Regex pattern to extract scores
    score_pattern = r'(Efficiency|Completeness|Style|Documentation):\s*([\d.]+)'

    # Extract scores and store as metadata
    metadata = {
        "Scores": {match[0]: float(match[1]) for match in re.findall(score_pattern, processed_review_text)}
    }

    # Regex pattern to split the review by keywords
    split_pattern = r'\b(' + '|'.join(keywords) + r')\b'
    split_text = re.split(split_pattern, processed_review_text)

    # Extract relevant sections
    sections = []
    for i in range(1, len(split_text), 2):
        section_title = split_text[i]
        section_content = split_text[i + 1].strip()
        sections.append({
            "Title": section_title,
            "Content": section_content
        })

    # Add metadata to the result
    return {"Metadata": metadata, "Sections": sections}

