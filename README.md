# CampusPing

CampusPing is an automated notification and information retrieval system tailored for students of NSUT (Netaji Subhas University of Technology), New Delhi. It monitors the college's official site for new notices, processes them, and sends relevant notifications to users based on their preferences.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Monitoring:** Checks for new notices every 10 minutes.
- **OCR and Text Extraction:** Applies OCR to extract text from image-based PDFs using Tesseract.
- **Notice Summarization:** Summarizes notices using the `facebook/bart-large-cnn` model via Hugging Face API.
- **User-Specific Notifications:** Sends notices based on user-selected tags (e.g., B.Tech, Backlogs).
- **PDF Downloads:** Supports downloading of notice PDFs.
- **Web Interface:** Provides a user-friendly web interface for interaction.

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
   - [Ghostscript](https://ghostscript.com/releases/gsdnld.html) (for processing PDFs)
   - [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (for OCR)

5. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

- **Fetching Notices:** Automatically handled by the system every 10 minutes.
- **Summarization:** Summaries are generated using the `facebook/bart-large-cnn` model through the Hugging Face API.
- **Notifications:** Sent to users based on their chosen preferences and tags.

## Contributing

Contributions are welcome. Please follow the [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
