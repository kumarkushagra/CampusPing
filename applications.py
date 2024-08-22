import os

# Install Ghostscript
os.system("apt-get update && apt-get install -y ghostscript")

# Install Tesseract
os.system("apt-get install -y tesseract-ocr")
