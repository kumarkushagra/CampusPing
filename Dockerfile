# Use a base image with Python
FROM python:3.12-slim

# Install necessary packages for Tesseract and Ghostscript, and build essentials
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    wget \
    apt-transport-https \
    gnupg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ghostscript
RUN wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs950/ghostscript-9.50-linux-x86_64.tgz && \
    tar -xvf ghostscript-9.50-linux-x86_64.tgz && \
    mv ghostscript-9.50-linux-x86_64/gs-950-linux-x86_64 /usr/local/bin/gs && \
    rm -rf ghostscript-9.50-linux-x86_64*

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port if needed (optional, specify if your app uses a specific port)
# EXPOSE 8000

# Run the main.py script
CMD ["python", "main.py"]
