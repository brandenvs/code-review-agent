import psycopg2
import fitz  # PyMuPDF
import re
from pathlib import Path
import os
from PyPDF2 import PdfReader
import json
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean up extracted text by removing unnecessary whitespace and formatting."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,!?:)])', r'\1', text)
    text = re.sub(r'(\()\s+', r'\1', text)
    return text.strip()

def identify_section(text: str, current_section: str) -> str:
    """Identify section headers in the text."""
    known_headers = [
        "Introduction", "Instructions", "Take note", "Auto-graded task",
        "Scope", "Default values", "Docstrings", "Why use functions?",
        "Output:", "Parameters:", "Returns:", "Hint:"
    ]

    for header in known_headers:
        if text.strip().startswith(header):
            return header

    # Look for patterns that might indicate a header
    header_patterns = [
        r'^([A-Z][A-Za-z\s]{2,50}:)',
        r'^([A-Z][A-Za-z\s]{2,50})$'
    ]

    for pattern in header_patterns:
        match = re.match(pattern, text.strip())
        if match:
            return match.group(1).strip()

    return current_section

def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    """Extracts structured content from a PDF and prepares JSON output."""
    structured_content = []

    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        current_section = "General Content"
        current_content = []

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            paragraphs = text.split('\n')

            for paragraph in paragraphs:
                if not paragraph.strip() or "Copyright" in paragraph:
                    continue

                clean_paragraph = clean_text(paragraph)
                potential_section = identify_section(clean_paragraph, current_section)

                if potential_section != current_section:
                    if current_content:
                        structured_content.append({
                            "section": current_section,
                            "content": " ".join(current_content).strip()
                        })
                        current_content = []
                    current_section = potential_section

                if clean_paragraph and not clean_paragraph.startswith(current_section):
                    current_content.append(clean_paragraph)

        # Add the last section
        if current_content:
            structured_content.append({
                "section": current_section,
                "content": " ".join(current_content).strip()
            })

    return structured_content

def save_structured_content_for_pgai(structured_content: List[Dict[str, str]], output_path: str):
    """Save structured content as a JSON file optimized for vector embedding."""
    pgai_ready_content = []

    for item in structured_content:
        pgai_ready_content.append({
            "text": item["content"],
            "metadata": {
                "section": item["section"]
            }
        })

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(pgai_ready_content, file, ensure_ascii=False, indent=2)

def process_pdf_for_pgai(pdf_path: str, output_json_path: str):
    """Main function to process PDF and generate JSON for vector embedding."""
    structured_content = extract_pdf_content(pdf_path)
    save_structured_content_for_pgai(structured_content, output_json_path)


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
