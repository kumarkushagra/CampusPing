import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = 'https://www.imsnsit.org/imsnsit/notifications.php'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Define a function to filter tr elements
def is_target_tr(tag):
    if tag.name != 'tr':
        return False
    # Check if the tr contains the specified structure
    first_td = tag.find('td', nowrap=True)
    second_td = tag.find('td', class_='list-data-focus')
    if first_td and second_td:
        font_tag = first_td.find('font', size='3')
        img_tag = first_td.find('img', src='images/newicon.gif')
        a_tag = second_td.find('a', href=True, title="NOTICES / CIRCULARS")
        font_tag_2 = a_tag.find('font', size='3') if a_tag else None
        return font_tag and img_tag and a_tag and font_tag_2
    return False

# Find all target tr elements
target_trs = soup.find_all(is_target_tr)

def create_csv_and_append_row(user_data):
    """
    Creates a new CSV file with specified columns if it doesn't exist and appends a new row.
    
    Args:
    filename (str): The name of the CSV file.
    user_data (list): A list containing data to append to the CSV.
    """
    # Define name of CSV file
    filename = "notice.csv"

    # Define column names
    columns = ['Date', 'Title', 'Publisher_info', 'pdf_link']
    
    # Check if the CSV file exists
    if not os.path.isfile(filename):
        # Create a DataFrame with the specified columns
        df = pd.DataFrame(columns=columns)
        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"{filename} has been created with columns: {', '.join(columns)}")
    
    # Load the existing CSV file
    df = pd.read_csv(filename)
    
    # Create a DataFrame for the new row
    new_row = pd.DataFrame([user_data], columns=columns)
    
    # Append new row using pd.concat
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    df.to_csv(filename, index=False, encoding='utf-8')

for tr in target_trs:
    row = []
    # Date
    date = tr.find('td').get_text(strip=True)
    row.append(date)

    # Title
    notice_title = tr.find('a').get_text(strip=True)
    row.append(notice_title)

    # Publisher info
    publisher_info = tr.find('b').get_text(strip=True).replace("Published By:  ", "")
    # publisher_info = [part.strip() for part in publisher_info.split(',')]
    row.append(publisher_info)

    # pdf link
    link = tr.find('a')['href']
    row.append(link)

    create_csv_and_append_row(row)




