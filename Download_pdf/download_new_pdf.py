import requests

def create_session_and_get_cookies(url):
    session = requests.Session()
    response = session.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return session

def download_document(session, url, output_path):
    # Get the document content using the session
    response = session.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Print response details for debugging
    print("Response URL:", response.url)
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)

    # Determine the file type from the response headers
    content_type = response.headers.get('Content-Type', '')
    print("Content-Type:", content_type)

    if 'application/pdf' in content_type:
        # If the content is already a PDF, save it directly
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Document saved as {output_path}")
    else:
        # If the content is not a PDF, print an error message
        print("The content is not a PDF. The response is:")
        print(response.text)

# URL of the notifications page and the document
notifications_url = 'https://www.imsnsit.org/imsnsit/notifications.php'
document_url = 'https://www.imsnsit.org/imsnsit/plum_url.php?qk7KimXU2qKPhxcpfYe8u0eo5n+rr8EW31QAO9Nu+VdHFCsAtZ2EZ7BZp1c/v3JOIYs5yY9zWzEU5nSLL7UyjL4GfRnoYkhSk34aJCNpMmAsAQmCGVODqTnV/SZa/MBGMX4WlWbi1fT1Zot3wsj35oPsFo1E4SJbPP5oLTXmkADXR3D7bjcLMlFwIuj1/eVUpuH1RyZssbqvtSKccATy0g=='  # Replace with your document URL
output_path = 'output_document.pdf'

# Create the session and get cookies
session = create_session_and_get_cookies(notifications_url)

# Download the document using the session
download_document(session, document_url, output_path)
