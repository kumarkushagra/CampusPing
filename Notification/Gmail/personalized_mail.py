import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'imsnotificationbot@gmail.com'
EMAIL_PASSWORD = 'gdxm cmzv mjpr dzyi'  # Use an app password if 2FA is enabled

def send_email(to_email, subject, body):
    """Send an email using Gmail's SMTP server."""
    try:
        # Create a MIME object
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {to_email}.")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def send_emails():
    # Read the CSV files
    user_data_df = pd.read_csv('user_data.csv')
    output_df = pd.read_csv('output.csv')

    # Get the extracted text of the last notice
    last_notice_text = output_df.iloc[-1]['extracted_text']
    print("Last notice text retrieved.")

    # Iterate over each user in user_data.csv
    for _, row in user_data_df.iterrows():
        name = row['Name']
        roll_number = row['Roll Number']
        email = str(row.get('Email', '')).strip()  # Ensure email is a string and handle NaN

        if not email or email == 'nan':
            print(f"Invalid or missing email for {name}. Skipping.")
            continue

        # Convert name and roll_number to strings and handle NaN values
        name = str(name) if pd.notna(name) else ''
        roll_number = str(roll_number) if pd.notna(roll_number) else ''

        # Initialize flags for sending emails
        name_found = False
        roll_number_found = False

        # Check if the name is found in the extracted text
        if name and re.search(re.escape(name), last_notice_text, re.IGNORECASE):
            name_found = True
            print(f"Name '{name}' found in the extracted text.")

        # Check if the roll number is found in the extracted text
        if roll_number and re.search(re.escape(roll_number), last_notice_text, re.IGNORECASE):
            roll_number_found = True
            print(f"Roll number '{roll_number}' found in the extracted text.")
        
        # Send a combined email if both name and roll number were found
        if name_found or roll_number_found:
            subject = "Notice Update"
            body = f"""Hello {name}, your {'name and roll number' if name_found and roll_number_found else 'name' if name_found else 'roll number'} was found in the latest notice. Please check it out!
Link: https://www.imsnsit.org/imsnsit/notifications.php
            """
            send_email(email, subject, body)

if __name__ == "__main__":
    send_emails()
