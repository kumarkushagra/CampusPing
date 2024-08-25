import os
import csv
import typing

CSV_FILE: typing.Final = 'output.csv'
USER_DATA_FILE: typing.Final = 'user_data.csv'

# Utility functions for CSV operations
def read_user_data() -> dict:
    user_data = {}
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                user_data = {
                    row['Chat ID']: {
                        'Name': row['Name'],
                        'Tags': row['Tags'],
                        'Roll Number': row['Roll Number'],
                        'Email': row.get('Email', ''),  # Handle case if Email is missing
                        'Phone Number': row.get('Phone Number', '')  # Handle case if Phone Number is missing
                    }
                    for row in reader
                }
        except Exception as e:
            print(f"Error reading user data: {e}")
    return user_data

def write_user_data(user_data: dict):
    try:
        with open(USER_DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["Chat ID", "Name", "Tags", "Roll Number", "Email", "Phone Number"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for chat_id, data in user_data.items():
                writer.writerow({
                    "Chat ID": chat_id,
                    "Name": data['Name'],
                    "Tags": data['Tags'],
                    "Roll Number": data['Roll Number'],
                    "Email": data.get('Email', ''),  # Handle case if Email is missing
                    "Phone Number": data.get('Phone Number', '')  # Handle case if Phone Number is missing
                })
    except Exception as e:
        print(f"Error writing user data: {e}")

def read_tags_from_csv() -> set:
    tags = set()
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                tags = {
                    tag.strip().strip('[]').strip("'")
                    for row in reader
                    for tag in row.get('tags', '').split(",") if tag.strip()
                }
        except Exception as e:
            print(f"Error reading tags: {e}")
    return tags

def read_notifications() -> list:
    notifications = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                notifications = [
                    {
                        'LLM_summary': row['LLM_summary'],
                        'link_to_notice': "https://www.imsnsit.org/imsnsit/notifications.php",
                        'tags': row['tags'].split(', ')
                    }
                    for row in reader
                ]
        except Exception as e:
            print(f"Error reading notifications: {e}")
    return notifications
