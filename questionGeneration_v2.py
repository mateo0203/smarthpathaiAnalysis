import os
import openai
import chromadb
from dotenv import load_dotenv
from helpers import extract_save_pdf
import google.generativeai as genai


load_dotenv()

# Load keys from environment variables
gemini_key = os.getenv('GEMINI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Configure OpenAI for embeddings
openai.api_key = openai_api_key

# Initialize Chroma DB
client = chromadb.Client()
collection = client.create_collection("pdf_chunks")  # Create or get collection for PDF chunks

# Extract and save PDF chunks
pdf_path = 'content/psych.pdf'
output_file = 'content/psychContent/content'
pdf_text = extract_save_pdf(pdf_path, start_page=5, end_page=30, chunk_size=5, output_file=output_file)

# Loop over saved text files in 'content/psychContent/' folder
for chunk_num in range(1, 6):  # Assuming 5 chunks, adjust range as needed
    file_path = f'content/psychContent/content_{chunk_num}.txt'
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    """
    # Step 1: Generate questions from the content using Gemini model
    response = model.generate_content(f"Create 5 questions from the following content: {content}")
    print(response.text)
    """
    
    # Step 2: Generate embedding using OpenAI embeddings model
    embedding = openai.Embedding.create(
        input=content,
        model="text-embedding-ada-002"
    )['data'][0]['embedding']  # Extract the embedding from OpenAI response
    
    # Step 3: Store the chunk and its embedding in Chroma DB
    collection.add(
        documents=[content],
        embeddings=[embedding],
        metadatas=[{"chunk_num": chunk_num}]  # Store additional metadata if needed
    )

print("Chunks and embeddings saved to Chroma DB.")
