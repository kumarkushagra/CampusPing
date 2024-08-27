import typing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import pandas as pd
import ast  # For safely evaluating string representations of all Tags

from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
SMTP_SERVER: typing.Final = 'smtp.gmail.com'
SMTP_PORT: typing.Final = 587
EMAIL_ADDRESS: typing.Final = 'imsnotificationbot@gmail.com'
EMAIL_PASSWORD: typing.Final = os.getenv('GMAIL_APP_PASSWORD')
USER_DATA_FILE: typing.Final = 'user_data.csv'
NOTIFICATIONS_FILE: typing.Final = 'output.csv'

async def send_emails_to_users():
    try:
        # Read notifications from the CSV file using pandas
        notifications_df = pd.read_csv(NOTIFICATIONS_FILE)
        if notifications_df.empty:
            print("No notifications available.")
            return

        # Convert 'email_sent' column to integer, defaulting to 0 if conversion fails
        notifications_df['email_sent'] = pd.to_numeric(notifications_df['email_sent'], errors='coerce').fillna(0).astype(int)

        # Filter notifications that have not been sent
        unsent_notifications_df = notifications_df[notifications_df['email_sent'] == 0]
        if unsent_notifications_df.empty:
            print("All notifications have already been sent.")
            return

        # Read user data from the CSV file using pandas
        user_data_df = pd.read_csv(USER_DATA_FILE)
        user_data = {}
        for _, row in user_data_df.iterrows():
            email = row.get('Email')
            if pd.isna(email) or email.strip() == '':
                continue
            email = email.strip()
            user_tags = row.get('Tags', '')
            user_tags = [tag.strip().lower() for tag in user_tags.split(',') if tag.strip()] if pd.notna(user_tags) else []
            user_data[email] = user_tags

        # Initialize the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Process each unsent notification
        for _, notification in unsent_notifications_df.iterrows():
            # Extract notification details
            summary = notification['LLM_summary'].strip()
            link = "https://www.imsnsit.org/imsnsit/notifications.php"
            tags = notification.get('tags', '')

            # Process tags
            if pd.isna(tags):
                tags = ''
            
            try:
                tags = ast.literal_eval(tags)
                if isinstance(tags, list):
                    tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
                else:
                    tags = []
            except (SyntaxError, ValueError):
                tags = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]

            notification_text = f"{summary}\n\n{link}\nTags: {', '.join(tags)}"
            print(f"Tags of the notification: {tags}")

            # Send notification to users based on tags
            for email, user_tags in user_data.items():
                if not tags or set(tags) & set(user_tags):
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = EMAIL_ADDRESS
                        msg['To'] = email
                        msg['Subject'] = 'Notice Update'
                        msg.attach(MIMEText(notification_text, 'plain'))

                        server.send_message(msg)
                        print(f"Email sent to {email}")
                    except Exception as e:
                        print(f"Failed to send email to {email}. Error: {e}")

            # Update the CSV file to mark the notification as sent
            notifications_df.loc[notifications_df['S. no.'] == notification['S. no.'], 'email_sent'] = 1

        # Save the updated notifications dataframe to CSV
        notifications_df.to_csv(NOTIFICATIONS_FILE, index=False)

        # Close the SMTP server
        server.quit()

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_emails_to_users())
