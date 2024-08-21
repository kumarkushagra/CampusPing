import pandas as pd
import os

def is_notice_existing(new_row):
    """
    Checks if the notice is already in the CSV file.
    
    Args:
    new_row (list): A list containing data for the new notice.
    
    Returns:
    bool: True if the notice already exists, False otherwise.
    """
    filename = "notice.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        new_row_df = pd.DataFrame([new_row], columns=df.columns)
        # Check for duplicate entries based on 'Date' and 'Title'
        for index, row in new_row_df.iterrows():
            if ((df['Date'] == row['Date']) & (df['Title'] == row['Title'])).any():
                return True
    return False

def create_csv_and_append_row(user_data):
    """
    Creates a new CSV file with specified columns if it doesn't exist and appends a new row.
    
    Args:
    user_data (list): A list containing data to append to the CSV.
    """
    # Define name of CSV file
    filename = "notice.csv"

    # Define column names
    columns = ['S.No','Date','Time', 'Title','Download status' ,'Publisher_info', 'pdf_link']
    
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