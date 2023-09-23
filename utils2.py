import PyPDF2
import spacy
import time
import openai
import re

# Initialize OpenAI API
openai.api_key = "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"

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Function to split PDF into text chunks
def split_pdf_into_text_chunks(pdf_path, max_tokens_per_chunk=1000):
    # Open the PDF file
    pdf_file = open(pdf_path, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    chunks = []
    current_chunk = ""
    current_token_count = 0

    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page
        page = pdf_reader.pages[page_num]
        page_text = remove_extra_whitespaces(page.extract_text())


        # Split the page text into sentences using spaCy
        doc = nlp(page_text)
        for sent in doc.sents:
            sent_text = sent.text
            
            # Calculate the token count locally
            sent_token_count = len(sent)
           # Check if adding the sentence would exceed the token limit
            if current_token_count + sent_token_count > max_tokens_per_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
                current_token_count = 0

            current_chunk += sent_text + " "
            current_token_count += sent_token_count

    # Add the remaining chunk, if any
    if current_chunk:
        chunks.append(current_chunk)

    # Close the PDF file
    pdf_file.close()

    return chunks

# Function to add chunks to the vector store with rate limiting
def add_chunks_to_vector_store(chunks, vStore, batch_size=5, delay=16):
    # Initialize variables
    batch = []
    total_tokens = 0

    # Iterate through each chunk
    for chunk in chunks:
        # Calculate the token count locally
        chunk_token_count = len(nlp(chunk))

        # Check if adding the chunk would exceed the token limit
        if total_tokens + chunk_token_count > 4096:
            # Process the current batch
            if batch:
                process_batch(batch, vStore)
                batch = []
                total_tokens = 0

            # Sleep to avoid rate limiting
            time.sleep(delay)

        batch.append(chunk)
        total_tokens += chunk_token_count

    # Process any remaining chunks
    if batch:
        process_batch(batch, vStore)

# Function to process a batch of chunks (e.g., add to vector store)
def process_batch(batch, vStore):
    # Process and add the batch to the vector store
    nodes = []
    for chunk in batch:
        doc = nlp(chunk)
        for sent in doc.sents:
            nodes.append({
                'page_content': sent.text,
                'metadata': {}
            })

    # Add the batch to the vector store
    vStore.add_documents(nodes)


# Function to remove unnecessary whitespaces
def remove_extra_whitespaces(text):
    # Remove leading and trailing whitespaces
    text = text.strip()

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    return text