
# CampusPing

CampusPing is an advanced, automated notification and information retrieval system designed for the students of NSUT (Netaji Subhas University of Technology), New Delhi. The platform continuously monitors the university's official site for new notices, processes them, and delivers personalized notifications to users based on their specific preferences.

This project is deployed on **Azure**, leveraging its robust infrastructure to ensure high availability and reliability.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Note](#note)

## Features

- **Automated Monitoring:** Continuously checks for new notices every 10 minutes.
- **OCR and Text Extraction:** Utilizes Tesseract for OCR to extract text from image-based PDFs.
- **Notice Summarization:** Uses the `facebook/bart-large-cnn` model via Hugging Face API to summarize notices effectively.
- **User-Specific Notifications:** Delivers notices based on user-selected categories (e.g., B.Tech, Backlogs).
- **PDF Downloads:** Allows easy downloading of notice PDFs.
- **Web Interface:** Offers an intuitive web interface for seamless user interaction.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/CampusPing.git
   cd CampusPing
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Additional Applications:**
   - [Ghostscript](https://ghostscript.com/releases/gsdnld.html) (for PDF processing)
   - [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (for Optical Character Recognition)

5. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

- **Fetching Notices:** Automatically managed by the system every 10 minutes.
- **Summarization:** Notices are summarized using the `facebook/bart-large-cnn` model through the Hugging Face API.
- **Notifications:** Notifications are sent to users based on their selected tags and preferences.

## Note

This project integrates services from HuggingFace (for notice summarization using an LLM), Telegram (for sending notifications), and Gmail (for sending emails). The necessary API keys are securely stored in a `.env` file located in the root directory.

The format of the `.env` file is as follows:

```plaintext
SECRET_KEY='your_secret_key'
TELEGRAM_API_TOKEN='your_telegram_api_token'
GMAIL_APP_PASSWORD='your_gmail_app_password'
HUGGING_FACE_KEY='your_hugging_face_key'
```

**Security Notice:** We have invalidated any API keys that were visible in previous commits. Please ensure your `.env` file is updated with new and secure API keys.

**Important:** Make sure to replace the placeholder values with your actual credentials and API keys.

---
