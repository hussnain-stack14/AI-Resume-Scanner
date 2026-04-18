import pdfplumber
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def calculate_similarity(resume_text, job_desc_text):
    """
    Calculates the cosine similarity between the resume text 
    and job description using TF-IDF Vectorization.
    """
    if not resume_text or not job_desc_text:
        return 0.0
    
    # Create TF-IDF Vectorizer with stop words removal
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Fit and transform the texts
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Convert similarity score to a percentage
    match_percentage = round(similarity_matrix[0][0] * 100, 2)
    return match_percentage

def get_keyword_density(text, top_n=10):
    """
    Calculates the frequency of non-stopword keywords in the text.
    """
    if not text:
        return []
    
    # Enhanced stop words list
    stop_words = {
        'and', 'the', 'a', 'to', 'for', 'with', 'in', 'on', 'at', 'by', 'of', 'from', 'as', 'is', 'are', 'was', 'were', 
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'but', 'if', 'or', 'because', 'as', 'until', 
        'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 
        'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 
        'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 
        'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'using', 'experience', 'knowledge', 
        'ability', 'skills', 'work', 'working', 'team', 'ideal', 'candidate', 'requirements', 'responsibilities'
    }
    
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    
    counts = Counter(filtered_words)
    return counts.most_common(top_n)
