# ResumeAI Pro | AI-Powered Career Assistant

A state-of-the-art web application built with Python and Streamlit. It leverages **Google Gemini's Generative AI** to analyze an uploaded resume against a targeted job description, providing deep semantic matching, skill gap analysis, ATS issue detection, and an interactive AI agent chat.

## Features

- **Generative AI Analysis**: Uses Google Gemini to intelligently evaluate the contextual fit between a resume and a job description.
- **Interactive AI Agent**: Chat directly with the embedded AI to rewrite bullet points, write cover letters, and get personalized interview coaching.
- **Portfolio Demo Mode**: Instantly test out the fully populated dashboard without an API key using the integrated mock-data demo mode.
- **Modern UI/UX**: Premium dual-theme interface featuring "Auto-Dark" mode and a beautiful "Sunrise Amber" professional light theme, complete with glassmorphism aesthetics.
- **Secure Processing**: Privacy-focused file handling that deletes temporary PDF data immediately after text extraction.

## Project Structure

- `app.py`: The Streamlit frontend and main AI agent entry point.
- `utils.py`: Utility functions for robust PDF text extraction and pre-processing.
- `style.css` / `style_light.css`: Custom CSS injected into Streamlit for high-end styling.
- `requirements.txt`: Required dependencies (Streamlit, google-generativeai, pdfplumber).

## Installation & Setup

1. Make sure you have **Python 3.8+** installed.
2. Clone or open this repository folder.
3. Open a terminal / command prompt.
4. Optional but recommended: Create and activate a virtual environment:
   ```bash
   python -m venv venv312
   # On Windows PowerShell:
   .\venv312\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv312/bin/activate
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

This will automatically launch the UI in your default web browser.

*Note: For full AI functionality, retrieve a free API Key from [Google AI Studio](https://aistudio.google.com/app/apikey) and enter it in the application's sidebar. If you run it without an API key, it will smoothly fall back to a fully populated Mock Portfolio Demo Mode.*
