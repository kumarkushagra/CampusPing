# Use a lightweight Python image as the base
FROM python:3.12-slim

# Install Ghostscript and Tesseract OCR
RUN apt-get update && apt-get install -y \
    ghostscript \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your Python script
CMD ["python", "main.py"]
