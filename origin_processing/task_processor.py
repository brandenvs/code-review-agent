from PyPDF2 import PdfReader
import re
import json
from typing import List, Dict

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    return text.strip()


def identify_section(text: str) -> str:
    known_headers = [
        "Instructions",
        "Take note",
        "Auto-graded task",
        "Scope",
        "Default values",
        "Docstrings",
        "Why use functions?",
        "Programming With User-Defined Functions"
    ]
    
    for header in known_headers:
        if header.lower() in text.lower()[:100]:  # Check first 100 chars
            return header

    # Regex patterns
    header_patterns = [
        r'^([A-Z][A-Za-z\s]{2,50}:)',  # Capitalized words followed by colon
        r'^([A-Z][A-Za-z\s]{2,50})\n',  # Capitalized words followed by newline
    ]
    
    for pattern in header_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return "Content"


def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    structured_content = []
    
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        current_section = None
        current_content = []
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            paragraphs = text.split('\n')
            
            for paragraph in paragraphs:
                if not paragraph.strip() or "Copyright" in paragraph:
                    continue
                
                clean_paragraph = clean_text(paragraph)
                
                potential_section = identify_section(clean_paragraph)
                
                if potential_section != "Content" or not current_section:
                    if current_section and current_content:
                        structured_content.append({
                            "page": page_num + 1,
                            "section": current_section,
                            "content": " ".join(current_content)
                        })
                        current_content = []
                    current_section = potential_section
                
                if clean_paragraph:
                    current_content.append(clean_paragraph)
            
            if current_section and current_content:
                structured_content.append({
                    "page": page_num + 1,
                    "section": current_section,
                    "content": " ".join(current_content)
                })
                current_content = []
    
    return structured_content


def save_structured_content(structured_content: List[Dict[str, str]], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(structured_content, file, ensure_ascii=False, indent=2)
