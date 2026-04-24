import pdfplumber
import re

def extract_text_from_pdf(file_path):
    """
    Extracts text from a given PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    return text

def clean_text(text):
    """
    Cleans the input text by removing URLs, special characters, 
    and extra formatting, converting everything to lowercase.
    """
    if not text:
        return ""
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S*@\S*\s?', '', text)
    # Remove special characters but keep those common in tech (++, #, ., /) and numbers
    text = re.sub(r'[^a-zA-Z0-9\s#+\./]', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text
