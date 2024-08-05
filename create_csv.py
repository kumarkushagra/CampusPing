import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from create_csv_and_append_row import create_csv_and_append_row

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




def update_CSV():
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



if __name__ == "__main__":
    
    # defining soup
    url = 'https://www.imsnsit.org/imsnsit/notifications.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all target tr elements
    target_trs = soup.find_all(is_target_tr)
    update_CSV()
