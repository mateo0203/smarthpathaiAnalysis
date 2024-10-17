import os
import google.generativeai as genai
from dotenv import load_dotenv
from helpers import extract_save_pdf


load_dotenv()

#openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=gemini_key)

model = genai.GenerativeModel("gemini-1.5-flash")

pdf_path = 'content/psych.pdf'
output_file = 'content/psychContent/content'
pdf_text = extract_save_pdf(pdf_path, start_page=5, end_page=30, chunk_size=5, output_file=output_file)

with open('content/psychContent/content_2.txt', 'r', encoding='utf-8') as file:
    content = file.read()

response = model.generate_content(f"Create 5 questions from the following content: {content}")

print(response.text)