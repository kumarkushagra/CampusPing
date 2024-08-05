import pandas as pd
import os

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