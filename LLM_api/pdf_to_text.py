import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Get the total number of pages
    num_pages = len(pdf_document)
    # Limit to a maximum of 10 pages
    pages_to_read = min(10, num_pages)
    
    text = ""
    
    # Iterate through each page in the PDF
    for page_num in range(pages_to_read):
        # Get the page
        page = pdf_document.load_page(page_num)
        # Extract text from the page
        text += page.get_text()
    
    # Close the PDF document
    pdf_document.close()
    
    return text

if __name__=="__main__":
    pdf_path = r"D:\PROJECT\CampusPing\Download_pdf\testing_new.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)