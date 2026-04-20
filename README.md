# AI Resume Scanner

An AI-powered web application built with Python and Streamlit. It analyzes an uploaded resume against a provided job description by calculating a match score using TF-IDF and identifies extracted vs. missing skills.

## Project Structure

- `app.py`: The Streamlit frontend and main entry point.
- `utils.py`: Contains logic for extracting text from PDF and calculating cosine similarity matching using Scikit-Learn.
- `skills.py`: Contains a predefined list of common skills and logic to extract them safely for checking against the resume and job description.
- `requirements.txt`: List of required Python packages to run the project.

## Installation & Setup

1. Make sure you have **Python 3.8+** installed.
2. Clone or open this repository folder.
3. Open a terminal / command prompt.
4. Optional but recommended: Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

After installing dependencies, run the application using Streamlit:

```bash
streamlit run app.py
```

This will automatically launch the UI in your default web browser (typically at http://localhost:8501).

## Features

- Clean layout using Streamlit.
- Support for extracting textual data directly from PDF files.
- NLP-backed Match Score (TF-IDF vectorizer + Cosine Similarity comparison).
- Simple extraction logic for common technical and professional keywords.

## help

.\venv312\Scripts\Activate.ps1

pip install -r requirements.txt

streamlit run app.py
