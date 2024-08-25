import typing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import csv
import ast  # For safely evaluating string representations of Python literals

# Configuration
SMTP_SERVER: typing.Final = 'smtp.gmail.com'
SMTP_PORT: typing.Final = 587
EMAIL_ADDRESS: typing.Final = 'imsnotificationbot@gmail.com'
EMAIL_PASSWORD: typing.Final = 'gdxm cmzv mjpr dzyi'  # Use your generated app password here
USER_DATA_FILE: typing.Final = 'user_data.csv'
NOTIFICATIONS_FILE: typing.Final = 'output.csv'

async def send_email_to_users():
    try:
        # Read notifications from the CSV file
        with open(NOTIFICATIONS_FILE, mode='r', encoding='utf-8') as file:
            reader = list(csv.DictReader(file))
            if not reader:
                print("No notifications available.")
                return

            # Get the last notification
            latest_notification = reader[-1]
            if latest_notification.get('email_sent') == '1':
                print("Notice already sent.")
                return

            # Extract notification details
            summary = latest_notification.get('LLM_summary', '').strip()
            link = "https://www.imsnsit.org/imsnsit/notifications.php"
            tags = latest_notification.get('tags')

            # Process tags
            if tags is None:
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

        # Read user data from the CSV file
        user_data = {}
        with open(USER_DATA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row.get('Email')
                if email is None or email.strip() == '':
                    continue
                email = email.strip()
                user_tags = row.get('Tags', '')
                user_tags = [tag.strip().lower() for tag in user_tags.split(',') if tag.strip()] if user_tags else []
                user_data[email] = user_tags

        # Initialize the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

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
        with open(NOTIFICATIONS_FILE, mode='r+', encoding='utf-8', newline='') as file:
            reader = list(csv.DictReader(file))
            fieldnames = reader[0].keys()
            file.seek(0)
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row.get('S. no.') == latest_notification.get('S. no.'):
                    row['email_sent'] = '1'
                writer.writerow(row)
            file.truncate()  # Truncate the file to remove any leftover data from previous writes

        # Close the SMTP server
        server.quit()

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_email_to_users())
