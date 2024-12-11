import streamlit as st
import requests
from newspaper import Article
import fitz  # PyMuPDF
import json
import os

# Define login credentials
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            font-family: Arial, sans-serif;
        }
        .reportview-container {
            background-color: transparent;
        }
        .sidebar .sidebar-content {
            background-color: #333;
            color: #fff;
        }
        .main .block-container {
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease-in-out;
        }
        .main .block-container:hover {
            background-color: #f9f9f9;
        }
        h1, h2, h3 {
            color: #007bff;
            font-weight: bold;
        }
        .stButton button {
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #0056b3;
        }
        .stTextInput input, .stTextArea textarea {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 0.5rem;
            transition: border-color 0.3s ease;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #007bff;
            outline: none;
        }
        .stSelectbox select {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Path to store user credentials
USER_DATA_FILE = 'user_data.json'

# Load existing user data (if any)
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data to file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)

# Streamlit app logic for signup and login
def signup_page():
    st.title('Signup')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if st.button('Sign Up'):
        # Check if the username already exists
        user_data = load_user_data()
        if username in user_data:
            st.error('Username already exists. Please choose another one.')
        elif password != confirm_password:
            st.error('Passwords do not match.')
        else:
            # Add the new user to the data
            user_data[username] = password
            save_user_data(user_data)
            st.success('Signup successful! You can now log in.')

def login_page():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        user_data = load_user_data()
        if username in user_data and user_data[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['show_login'] = False
            st.session_state['username'] = username
            st.success('Login successful!')
        else:
            st.error('Incorrect username or password')
def main_page():
    st.title('Credibility Check for Articles, Newspapers, Research Papers, and PDFs')
    
    input_type = st.radio("Select the input type", ["URL", "Text"])
    
    if input_type == "URL":
        url = st.text_input("Enter the URL of the article, newspaper, research paper, or PDF:")
        source_type = st.selectbox("Select the type of content", ["Article", "Newspaper", "Research Paper", "PDF"])
        
        if st.button('Process URL'):
            if url:
                if source_type == "Article":
                    process_article(url)
                elif source_type == "Newspaper":
                    process_newspaper(url)
                elif source_type == "Research Paper" and url.lower().endswith(".pdf"):
                    process_research_paper(url)
                elif source_type == "PDF" and url.lower().endswith(".pdf"):
                    process_pdf(url)
                else:
                    st.warning("Please provide a valid URL and select the appropriate type of content.")
            else:
                st.warning("Please enter a URL.")
    
    elif input_type == "Text":
        text = st.text_area("Paste the text of the article here:")
        
        if st.button('Process Text'):
            if text:
                # Check credibility of the pasted text
                credibility = check_text_credibility(text)
                st.subheader("Text Details")
                st.write("Text:", text)
                st.write("Credibility:", credibility)
            else:
                st.warning("Please paste the text of the article.")

def process_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        st.subheader("Article Details")
        st.write("Title:", article.title)
        st.write("Authors:", article.authors)
        st.write("Publish Date:", article.publish_date)
        if article.top_image:
            st.image(article.top_image, caption="Top Image", use_container_width=True)
        st.write("Article Text:", article.text)
        
        # Check credibility
        credibility = check_credibility(article)
        st.write("Credibility:", credibility)
    except Exception as e:
        st.error(f"An error occurred while processing the article: {e}")

def process_newspaper(url):
    try:
        process_article(url)  # Newspapers are processed similarly to articles
    except Exception as e:
        st.error(f"An error occurred while processing the newspaper: {e}")

def process_research_paper(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Open the PDF
        pdf_file = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
        
        if text.strip() == "":
            st.warning("No text found in the research paper.")
        else:
            st.subheader("Research Paper Details")
            st.write("Text from Research Paper:", text)
            
            # Check credibility
            credibility = check_research_paper_credibility(text)
            st.write("Credibility:", credibility)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the PDF: {e}")
    except fitz.FitzError as e:
        st.error(f"An error occurred while processing the PDF: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def process_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Open the PDF
        pdf_file = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
        
        if text.strip() == "":
            st.warning("No text found in the PDF.")
        else:
            st.subheader("PDF Document Details")
            st.write("Text from PDF:", text)
            
            # Check credibility
            credibility = check_pdf_credibility(text)
            st.write("Credibility:", credibility)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the PDF: {e}")
    except fitz.FitzError as e:
        st.error(f"An error occurred while processing the PDF: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Credibility checking functions
def check_credibility(article):
    # Basic heuristics to determine credibility
    if article.publish_date and article.authors:
        return "Reliable"
    return "Unreliable"

def check_research_paper_credibility(text):
    # Simple example: check for the presence of keywords or structure
    if "abstract" in text.lower() and "introduction" in text.lower():
        return "Reliable"
    return "Unreliable"

def check_pdf_credibility(text):
    # Simple example: check for presence of metadata or keywords
    if "introduction" in text.lower() or "conclusion" in text.lower():
        return "Reliable"
    return "Unreliable"

def check_text_credibility(text):
    # Basic credibility check based on text content
    if "author" in text.lower() or "source" in text.lower():
        return "Reliable"
    return "Unreliable"

# Main logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_page()
else:
    st.sidebar.title("Login/Signup")
    login_or_signup = st.sidebar.radio("Choose an option", ["Login", "Signup"])
    if login_or_signup == "Login":
        login_page()
    else:
        signup_page()
