import PyPDF2
import re
import json
from typing import List, Dict

def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    structured_content = []
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            
            # Split the text into sections based on headers
            sections = re.split(r'\n(?=[A-Z][A-Z\s]+:)', text)
            
            for section in sections:
                # Extract the section title and content
                match = re.match(r'([A-Z][A-Z\s]+):(.*)', section, re.DOTALL)
                if match:
                    title, content = match.groups()
                else:
                    title, content = "UNNAMED SECTION", section
                
                structured_content.append({
                    "page": page_num,
                    "section": title.strip(),
                    "content": content.strip()
                })
    
    return structured_content

def save_structured_content(structured_content: List[Dict[str, str]], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(structured_content, file, ensure_ascii=False, indent=2)

def main():
    pdf_path = "data/T06 - Programming with User-defined Functions/DJ24100016307/10-023_Programming with User-defined Functions.pdf"
    output_path = "structured_content.json"
    
    structured_content = extract_pdf_content(pdf_path)
    save_structured_content(structured_content, output_path)
    
    print(f"Structured content has been saved to {output_path}")

if __name__ == "__main__":
    main()

