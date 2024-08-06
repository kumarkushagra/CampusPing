import ocrmypdf

def pdf_to_text_pdf(pdf_path):
    ocrmypdf.ocr(pdf_path, pdf_path)