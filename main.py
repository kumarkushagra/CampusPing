import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os

CSV_FILE = 'notices.csv'

def fetch_notices():
    url = 'https://www.imsnsit.org/imsnsit/notifications.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    notices = []

    for row in soup.select('tbody tr'):
        columns = row.find_all('td')
        if len(columns) >= 3: 
            date = columns[0].text.strip()
            subject = columns[1].text.strip()
            link = columns[1].find('a')['href'].strip() if columns[1].find('a') else ''
            published_by = columns[2].text.strip()

            notices.append({
                'Date': date,
                'Subject': subject,
                'Link': link,
                'Published by': published_by
            })
    
    return notices

def load_existing_notices():
    try:
        if os.stat(CSV_FILE).st_size == 0:
            return []
        return pd.read_csv(CSV_FILE).to_dict('records')
    except FileNotFoundError:
        return []

def save_notices_to_csv(notices):
    df = pd.DataFrame(notices)
    df.to_csv(CSV_FILE, index=False)

def append_notices_to_csv(notices):
    df = pd.DataFrame(notices)
    df.to_csv(CSV_FILE, mode='a', header=False, index=False)

def check_for_updates():
    existing_notices = load_existing_notices()
    existing_subjects = {notice['Subject'] for notice in existing_notices}

    new_notices = fetch_notices()
    updated_notices = [notice for notice in new_notices if notice['Subject'] not in existing_subjects]

    if updated_notices:
        print(f"Found {len(updated_notices)} new notice(s) at {datetime.now()}!")
        append_notices_to_csv(updated_notices)
    else:
        print(f"No new notices found at {datetime.now()}.")

def main():
    # Check if the CSV file exists and create it if it doesn't
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        print(f"Creating new CSV file at {datetime.now()}.")
        notices = fetch_notices()
        save_notices_to_csv(notices)

    # Set the interval (in seconds) for checking updates
    interval = 300  # Check every 5 minutes

    while True:
        check_for_updates()
        time.sleep(interval)

if __name__ == "__main__":
    main()




















################################################
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os

CSV_FILE = 'notices.csv'

def fetch_notices(limit=20):
    url = 'https://www.imsnsit.org/imsnsit/notifications.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    notices = []

    for i, row in enumerate(soup.select('tbody tr')):
        if i >= limit:
            break
        columns = row.find_all('td')
        if len(columns) >= 3: 
            date = columns[0].text.strip()
            subject = columns[1].text.strip()
            link = columns[1].find('a')['href'].strip() if columns[1].find('a') else ''
            published_by = columns[2].text.strip()

            notices.append({
                'Date': date,
                'Subject': subject,
                'Link': link,
                'Published by': published_by
            })
    
    return notices

def initialize_csv():
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        with open(CSV_FILE, 'w') as file:
            file.write('Date,Subject,Link,Published by\n')

def load_existing_notices():
    try:
        return pd.read_csv(CSV_FILE).to_dict('records')
    except pd.errors.EmptyDataError:
        return []

def save_notices_to_csv(notices):
    df = pd.DataFrame(notices)
    df.to_csv(CSV_FILE, mode='w', index=False)

def append_notices_to_csv(notices):
    df = pd.DataFrame(notices)
    df.to_csv(CSV_FILE, mode='a', header=False, index=False)

def check_for_updates():
    existing_notices = load_existing_notices()
    existing_subjects = {notice['Subject'] for notice in existing_notices}

    new_notices = fetch_notices()
    updated_notices = [notice for notice in new_notices if notice['Subject'] not in existing_subjects]

    if updated_notices:
        print(f"Found {len(updated_notices)} new notice(s) at {datetime.now()}!")
        append_notices_to_csv(updated_notices)
    else:
        print(f"No new notices found at {datetime.now()}.")

def main():
    # Initialize CSV file with headers if it doesn't exist or is empty
    initialize_csv()

    # Fetch initial notices and save them if the CSV is empty
    if os.stat(CSV_FILE).st_size == 0:
        print(f"Creating new CSV file at {datetime.now()}.")
        notices = fetch_notices()
        save_notices_to_csv(notices)

    # Set the interval (in seconds) for checking updates
    interval = 300  # Check every 5 minutes

    while True:
        check_for_updates()
        time.sleep(interval)

if __name__ == "__main__":
    main()
