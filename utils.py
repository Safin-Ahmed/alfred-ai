import PyPDF2
import os
import re


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, "rb") as pdf_file: 
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()        
    return split_text_into_chunks(text)


# Function to split text into chunks based on line breaks
def split_text_into_chunks(text, lines_per_chunk=30):
    lines = text.split("\n")
    chunks = []

    for i in range(0, len(lines), lines_per_chunk):
        chunk = " ".join(lines[i:i+lines_per_chunk])
        chunks.append(chunk)
    
    return chunks


# Function to remove unnecessary whitespaces
def remove_extra_whitespaces(text):
    # Remove leading and trailing whitespaces
    text = text.strip()

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    return text

# Function to extract text from multiple PDF files in a directory
def extract_text_from_pdf_list(dir):
    pdf_files = [f for f in os.listdir(dir) if f.endswith(".pdf")]

    texts = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(dir, pdf_file)
        extracted_text = extract_text_from_pdf(pdf_path)
        texts.append(remove_extra_whitespaces(extracted_text))
    
    return texts





