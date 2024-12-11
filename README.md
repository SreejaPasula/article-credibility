# Credibility Checker Web App

This is a Streamlit-based web application designed to check the credibility of articles, newspapers, research papers, and PDFs. The app also supports user authentication through a login and signup system.

---

## Features

1. **User Authentication**:
   - Users can sign up with a unique username and password.
   - Login functionality ensures secure access to the app.

2. **Content Analysis**:
   - Supports processing URLs and text directly entered by users.
   - Handles different types of input, including:
     - Articles
     - Newspapers
     - Research Papers
     - PDFs

3. **Credibility Checking**:
   - Evaluates credibility based on basic heuristics:
     - Articles are checked for publish date and authorship.
     - Research papers are validated for common structural components (e.g., abstract, introduction).
     - PDFs are analyzed for text metadata like "introduction" or "conclusion."
     - Text content credibility is checked for keywords like "author" or "source."

4. **Stylish User Interface**:
   - A modern and responsive design with CSS enhancements for a better user experience.

---

## How to Run

1. **Install Dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install streamlit requests newspaper3k pymupdf


### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
