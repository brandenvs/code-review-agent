import os

def process_file(file_path):
    """
    Process a single file (e.g., read its content and prepare it for embedding into the database).
    Replace this with your specific processing logic.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        max_length = 15
        if file_path.endswith('.py'):
            return content[:max_length] + "\n[Content truncated...]"
            print(f"Processing file: {file_path}")  # Replace with database embedding logic
        # Example: embedding(content, file_path)

def process_submission(submission_dir):
    """
    Recursively process all files within a given submission directory.
    """
    for root, dirs, files in os.walk(submission_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print(process_file(file_path))

def main(base_directory):
    """
    Process all submissions in the base directory.
    """
    for submission_name in os.listdir(base_directory):
        submission_path = os.path.join(base_directory, submission_name)
        if os.path.isdir(submission_path):
            print(f"Processing submission: {submission_name}")
            process_submission(submission_path)

if __name__ == "__main__":
    # Replace with the path to your base directory containing submissions
    base_directory = "A:\\workspace_001\\automating_code_reviews\\data"
    main(base_directory)
