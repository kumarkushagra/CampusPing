import requests
import csv
import os
from bs4 import BeautifulSoup

from fetch_and_save_html import fetch_and_save_html



# def parse_notices(html_file):
#     with open(html_file, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, 'html.parser')
    
#     notices = []
#     for row in soup.find_all('tr', class_='plum_head'):
#         columns = row.find_all('td')
#         if len(columns) < 4:
#             print(f"Skipping a row due to insufficient columns: {row}")
#             continue  # Skip rows that don't have enough columns
#         try:
#             notice = {
#                 'Date of upload': columns[0].text.strip(),
#                 'Department': columns[1].text.strip(),
#                 'Name of person': columns[2].text.strip(),
#                 'Link to notice': columns[3].find('a')['href'] if columns[3].find('a') else None
#             }
#             notices.append(notice)
#         except Exception as e:
#             print(f"Error processing row: {row}\n{e}")
#             continue  # Skip rows that cause errors
    
#     return notices

# def generate_csv(html_file, csv_file):
#     notices = parse_notices(html_file)
#     with open(csv_file, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Date of upload', 'Department', 'Name of person', 'Link to notice'])
#         writer.writeheader()
#         writer.writerows(notices)

# def append_new_notices(html_file, csv_file):
#     existing_notices = []
#     if os.path.exists(csv_file):
#         with open(csv_file, 'r', newline='', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 existing_notices.append(row)
    
#     new_notices = parse_notices(html_file)
#     new_notices_to_add = [notice for notice in new_notices if notice not in existing_notices]
    
#     if new_notices_to_add:
#         with open(csv_file, 'a', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=['Date of upload', 'Department', 'Name of person', 'Link to notice'])
#             writer.writerows(new_notices_to_add)

# # New function to fetch the site, store HTML, and process the notices
# def process_site_notices(url, html_file, csv_file):
#     fetch_and_save_html(url, html_file)
#     if not os.path.exists(csv_file):
#         generate_csv(html_file, csv_file)
#     else:
#         append_new_notices(html_file, csv_file)

# Usage:
url = 'https://www.imsnsit.org/imsnsit/notifications.php'
html_file = 'notices.html'
csv_file = 'notices.csv'
fetch_and_save_html(url, html_file)
# Process the site and update the notices CSV
# process_site_notices(url, html_file, csv_file)


