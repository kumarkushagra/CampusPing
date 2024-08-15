import requests
import certifi

try:
    response = requests.get('https://www.google.com', verify=certifi.where())
    print("Request was successful!")
    print(f"Status Code: {response.status_code}")
except requests.exceptions.SSLError as ssl_error:
    print(f"SSL Error: {ssl_error}")
except Exception as e:
    print(f"An error occurred: {e}")
