import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    text = ""
    
    # Iterate through each page in the PDF
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)
        # Extract text from the page
        text += page.get_text()
    
    # Close the PDF document
    pdf_document.close()
    
    return text

if __name__=="__main__":
    pdf_path = r"D:\PROJECT\CampusPing\Download_pdf\notice.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)