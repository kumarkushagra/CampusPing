# importing libraries
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from fpdf import FPDF
import tempfile  # New library for handling temporary files

# Defining the function where inputs: pdf_url, name_of_pdf to be saved as
def download_pdf(pdf_url, pdf_name="testing_new.pdf"):

    try:
        # Suppress SSL warnings
        warnings.simplefilter('ignore', InsecureRequestWarning)

        # Create a session
        with requests.Session() as session:
            # College Notice URL for establishing the session
            notifications_url = 'https://www.imsnsit.org/imsnsit/notifications.php'

            # Access the notifications page to establish the session and set cookies
            response = session.get(notifications_url, verify=False)

            # If session was established successfully:-
            if response.status_code == 200:
                # Fetch the file using the established session
                file_response = session.get(pdf_url, allow_redirects=True, verify=False, headers={
                    'Referer': notifications_url,  # Set Referer header if required
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'  # Mimic a real browser
                })

                # Check if the response was successful
                if file_response.status_code == 200:
                    # Check content type
                    content_type = file_response.headers.get('Content-Type')

                    if content_type == 'application/pdf':
                        # Save the PDF to the specified file path
                        with open(pdf_name, 'wb') as file:
                            file.write(file_response.content)
                    else:
                        # Handle non-PDF content (e.g., images)
                        if content_type.startswith('image/'):
                            # Save the image content to a temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
                                temp_image.write(file_response.content)
                                temp_image_path = temp_image.name

                            # Convert image to PDF
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.image(temp_image_path, x=10, y=10, w=pdf.w - 20)
                            pdf.output(pdf_name)
                        else:
                            # Handle other file types as text
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", size=12)
                            pdf.multi_cell(0, 10, file_response.text)
                            pdf.output(pdf_name)

    except Exception as e:
        print(f"An error occurred: {e}")

# Testing this function
if __name__ == "__main__":
    pdf_url = "https://www.imsnsit.org/imsnsit/plum_url.php?mfDNEsBxaV4NbJsNFasOFxAB108I2BD5EArJRrdE3BPopHlxDwfvQtZBMzUM5sGfQRMN/HULP+mphGx3RiRO92CBZLPF/SpgZEpzvU1pxvTjJyaEieWlUkcBbHWYzdpKACrRtFKmOQhkX3EX2a00EEsbVLZXl58YsKNrNgM7AWfyWVWkFzFyFc9i14/KU61HKEq597imuqEAzpagknGn6A=="
    pdf_name = "converted_file.pdf"
    download_pdf(pdf_url, pdf_name)
