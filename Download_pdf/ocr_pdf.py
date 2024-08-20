import ocrmypdf

def ocr_pdf(pdf_path):
    ocrmypdf.ocr(pdf_path, pdf_path, force_ocr=True)
    
    
if __name__ == "__main__":
    pdf_path= r"D:\PROJECT\CampusPing\Download_pdf\testing_new.pdf"
    ocr_pdf(pdf_path)