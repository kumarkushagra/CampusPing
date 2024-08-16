import ocrmypdf

def pdf_to_text_pdf(pdf_path):
    ocrmypdf.ocr(pdf_path, pdf_path, force_ocr=True)
    
    
if __name__ == "__main__":
    pdf_path= r"D:\PROJECT\CampusPing\Download_pdf\testing_new.pdf"
    save_pdf_path = r"D:\PROJECT\CampusPing\Download_pdf\testing_new_OCR.pdf"
    pdf_to_text_pdf(pdf_path)