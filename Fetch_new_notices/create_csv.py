import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from .create_csv_and_append_row import create_csv_and_append_row, is_notice_existing
from .is_target_tr import is_target_tr
from datetime import datetime
import time

# Important to avoid certificate verification
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings
# Define the URL
# url = 'https://www.imsnsit.org/imsnsit/notifications.php'
# response = requests.get(url)

# warnings.simplefilter('ignore', InsecureRequestWarning)

# response = requests.get('https://www.imsnsit.org/imsnsit/notifications.php', verify=False)

# soup = BeautifulSoup(response.content, 'html.parser')



def update_CSV(notice_csv_path = r'database\notice.csv'):
    # defining soup
    url = 'https://www.imsnsit.org/imsnsit/notifications.php'
    warnings.simplefilter('ignore', InsecureRequestWarning)
    response = requests.get('https://www.imsnsit.org/imsnsit/notifications.php', verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all target tr elements
    target_trs = soup.find_all(is_target_tr)
    
    
    for tr in target_trs:
        try:
            # Read the existing CSV file to find the last serial number
            existing_df = pd.read_csv(notice_csv_path)
            last_serial_number = existing_df["S.No"].max()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist or is empty, start with 0
            last_serial_number = 0
            
        serial_number = last_serial_number + 1
        
        row = []
        
        # Serial number
        row.append(serial_number)
        serial_number += 1  # Increment for the next notice
        
        # Date
        date = tr.find('td').get_text(strip=True)
        row.append(date)

        # Time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        row.append(current_time)

        # Title
        notice_title = tr.find('a').get_text(strip=True)
        row.append(notice_title)

        # Download status
        row.append(0)
        
        # Publisher info
        publisher_info = tr.find('b').get_text(strip=True).replace("Published By:  ", "")
        row.append(publisher_info)

        # pdf link
        link = tr.find('a')['href']
        row.append(link)

        # Check if the notice is already in the CSV
        if not is_notice_existing(row):
            create_csv_and_append_row(row)
            print("New notice added")
        else:
            break
def main():
    while True:
        # infinite loop
        update_CSV()

        # Wait for 20 minutes
        time.sleep(1200)  # 1200 seconds = 20 minutes

if __name__ == "__main__":
    # defining soup
    url = 'https://www.imsnsit.org/imsnsit/notifications.php'
    warnings.simplefilter('ignore', InsecureRequestWarning)
    response = requests.get('https://www.imsnsit.org/imsnsit/notifications.php', verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all target tr elements
    target_trs = soup.find_all(is_target_tr)
    main()
