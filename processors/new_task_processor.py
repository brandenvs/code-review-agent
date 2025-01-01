from PyPDF2 import PdfReader
import re
import json
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean up extracted text by removing unnecessary whitespace and formatting."""
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    return text.strip()

def identify_section(text: str) -> str:
    """Identify section headers in the text."""
    # List of known section headers from your PDF
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
    
    # Check for exact matches first
    for header in known_headers:
        if header.lower() in text.lower()[:100]:  # Check first 100 chars
            return header
    
    # Look for patterns that might indicate a header
    header_patterns = [
        r'^([A-Z][A-Za-z\s]{2,50}:)',  # Capitalized words followed by colon
        r'^([A-Z][A-Za-z\s]{2,50})\n',  # Capitalized words followed by newline
    ]
    
    for pattern in header_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return "Content"  # Default section name

def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    structured_content = []
    
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        current_section = None
        current_content = []
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Split text into paragraphs
            paragraphs = text.split('\n')
            
            for paragraph in paragraphs:
                # Skip empty paragraphs and copyright notices
                if not paragraph.strip() or "Copyright" in paragraph:
                    continue
                
                # Clean the paragraph
                clean_paragraph = clean_text(paragraph)
                
                # Check if this might be a new section
                potential_section = identify_section(clean_paragraph)
                
                if potential_section != "Content" or not current_section:
                    # Save previous section if it exists
                    if current_section and current_content:
                        structured_content.append({
                            "page": page_num + 1,
                            "section": current_section,
                            "content": " ".join(current_content)
                        })
                        current_content = []
                    current_section = potential_section
                
                # Add content to current section
                if clean_paragraph:
                    current_content.append(clean_paragraph)
            
            # Save section at page boundary if content exists
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

def main():
    pdf_path = "data/T03 – Data Types and Conditional Statements/UA24100016551/10-037 Data Types and Conditional Statements.pdf"  # Replace with your PDF path
    output_path = "structured_content.json"
    
    print("Extracting content from PDF...")
    structured_content = extract_pdf_content(pdf_path)
    
    # Print sections found for verification
    print("\nSections found:")
    for section in structured_content:
        print(f"\nPage {section['page']}")
        print(f"Section: {section['section']}")
        print(f"Content preview: {section['content'][:100]}...")
    
    print("\nSaving structured content...")
    save_structured_content(structured_content, output_path)
    
    print(f"\nContent has been structured and saved to {output_path}")

if __name__ == "__main__":
    main()