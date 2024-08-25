# Use a lightweight Python image as the base
FROM python:3.12-slim

# Install system dependencies including build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ghostscript \
    tesseract-ocr \
    tesseract-ocr-eng \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the Docker container
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt ./
COPY main.py ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run your Python script
CMD ["python", "main.py"]
