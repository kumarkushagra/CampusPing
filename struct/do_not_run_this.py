#DO NOT RUN THIS WITHOUT A REASON

import pandas as pd
import os

# Define the path to the file in the root directory
file_path = "D:\Projects\CampusPing\output.csv"  # Update this to the actual path if necessary

# Check if the file exists
if os.path.isfile(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Set all elements in the 'telegram_notification_sent' and 'email_sent' columns to 1
    df['telegram_notification_sent'] = 1
    df['email_sent'] = 1

    # Save the modified DataFrame back to the same CSV file
    df.to_csv(file_path, index=False)

    print(f"File successfully updated: {file_path}")
else:
    print(f"File {file_path} does not exist.")