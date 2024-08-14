# importing librariez
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Deining the function where inputs: pdf_url, name_of_pdf to be saved as
def download_pdf(pdf_url, pdf_name="notice.pdf"):

    try:
        # Suppress SSL warnings
        warnings.simplefilter('ignore', InsecureRequestWarning)

        # Create a session
        with requests.Session() as session:
            # college Notice URL for establishing the session
            notifications_url = 'https://www.imsnsit.org/imsnsit/notifications.php'

            # Access the notifications page to establish the session and set cookies
            response = session.get(notifications_url, verify=False)

            # if session was established successfully:-
            if response.status_code == 200:
                # Fetch the PDF using the established session
                pdf_response = session.get(pdf_url, allow_redirects=True, verify=False, headers={
                    'Referer': notifications_url,  # Set Referer header if required
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'  # Mimic a real browser
                })

                # Check if the response was successful and the file is a PDF
                if pdf_response.status_code == 200 and pdf_response.headers.get('Content-Type') == 'application/pdf':
                    # Save the PDF to the specified file path
                    with open(pdf_name, 'wb') as file:
                        file.write(pdf_response.content)

    except Exception as e:
        print(f"An error occurred: {e}")


# Testing this funtion
if __name__=="__main__":
    pdf_url = "https://www.imsnsit.org/imsnsit/plum_url.php?kR0Tf2aM5YVQRMOdyF1xGuExEC4z30kuFcaHt9rioqi33bMedqU6eakUHcZP1hP+T8Gg4xEZC9PHsypnl3V6pGjjmX1pLfhjxu5SAuHbfMUqGyE2G/6GRQJS+ZE3p2zZpBo9AYmR6IkUhLqeALMK853SU6eIUP4Apf3/MOXEg66s/a5i+qKdayM/nbjWibTa46m2aRT4dgoeuEHR8PYCcDDkh+Z904OPQWC3VbWNohY="
    pdf_name = ""
    download_pdf(pdf_url)