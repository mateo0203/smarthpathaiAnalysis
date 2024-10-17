import pdfplumber

def extract_save_pdf(pdf_path, start_page=0, end_page=None, chunk_size=5, output_file="contents"):
    """
    Extracts text from a PDF file and saves it into multiple text files, 
    each containing content from a specified number of pages (chunks).

    pdf_path (str) : The file path of the PDF to be processed.

    start_page (int) [optional]: The starting page number for extraction (default is 0, the first page).

    end_page (int) [optional]: The ending page number for extraction (default is None, which processes all pages).  

    chunk_size (int) [optional]: Number of pages to include in each output text file (default is 5).

    output_file (str): The base name for the output text files
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        chunk_number = 1
        output_name = f"{output_file}_{chunk_number}.txt"
        pages_to_extract = pdf.pages[start_page:end_page] if end_page else pdf.pages
        for i, page in enumerate(pages_to_extract):
            print(f"Processing page {i+1} of {len(pages_to_extract)} pages")
            text += page.extract_text()
            if (i+1) % chunk_size == 0:
                with open(output_name, 'w', encoding='utf-8') as f:
                    f.write(text)
                chunk_number += 1
                output_name = f"{output_file}_{chunk_number}.txt"
                text = ''
        if text:
            with open(output_name, 'w', encoding='utf-8') as f:
                f.write(text)