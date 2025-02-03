import pdfplumber
import docx
import requests
from bs4 import BeautifulSoup
import io  # Import io module for handling byte streams

def extract_text(content, filename):
    text = ""

    if filename.endswith(".pdf"):
        # Convert bytes to file-like object
        file_stream = io.BytesIO(content)
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

    elif filename.endswith(".docx"):
        file_stream = io.BytesIO(content)
        doc = docx.Document(file_stream)
        text = "\n".join([para.text for para in doc.paragraphs])

    else:
        # Assume it's a plain text file or an unknown format
        text = content.decode("utf-8")

    return text
