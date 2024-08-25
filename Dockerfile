# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install necessary packages including Tesseract and Ghostscript
RUN apt-get update && \
    apt-get install -y tesseract-ocr ghostscript && \
    apt-get clean

# Create a directory for the application
WORKDIR /app

# Copy the application's requirements file to the Docker image
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the Docker image
COPY . /app

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
