#!/bin/bash
set -e

# Update and install Ghostscript and Tesseract
sudo apt-get update
sudo apt-get install -y ghostscript tesseract-ocr tesseract-ocr-eng
