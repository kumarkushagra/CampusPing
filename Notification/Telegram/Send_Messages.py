import typing
from telegram import Bot
import asyncio
import csv
import ast  # For safely evaluating string representations of Python literals

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
USER_DATA_FILE: typing.Final = 'user_data.csv'
NOTIFICATIONS_FILE: typing.Final = 'output.csv'

async def send_message_to_chat_ids():
    bot = Bot(token=TOKEN)

    try:
        # Read notifications from the CSV file
        notifications = []
        with open(NOTIFICATIONS_FILE, mode='r', encoding='utf-8') as file:
            reader = list(csv.DictReader(file))
            if not reader:
                print("No notifications available.")
                return

            # Get the last notification
            latest_notification = reader[-1]
            if latest_notification.get('telegram_notification_sent') == '1':
                print("Notice already sent.")
                return

            # Extract notification details
            summary = latest_notification.get('LLM_summary', '').strip()
            link = "https://www.imsnsit.org/imsnsit/notifications.php"
            tags = latest_notification.get('tags', '').strip()

            # Process tags
            try:
                # Evaluate the tags safely to handle extra characters
                tags = ast.literal_eval(tags)
                if isinstance(tags, list):
                    tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
                else:
                    tags = []
            except (SyntaxError, ValueError):
                # Fallback in case the tags are not evaluable
                tags = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]

            notification_text = f"{summary}\n\n{link}\nTags: {', '.join(tags)}"
            print(f"Tags of the notification: {tags}")

        # Read user data from the CSV file
        chat_tags = {}
        with open(USER_DATA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                chat_id = row.get('Chat ID', '').strip()
                user_tags = row.get('Tags', '').strip()
                if user_tags:
                    user_tags = [tag.strip().lower() for tag in user_tags.split(',') if tag.strip()]
                else:
                    user_tags = []
                chat_tags[chat_id] = user_tags

        # Send notification to users based on tags
        for chat_id, user_tags in chat_tags.items():
            if not tags:  # If no tags, send to all users
                try:
                    await bot.send_message(chat_id=chat_id, text=notification_text)
                    print(f"Message sent to chat ID {chat_id}")
                except Exception as e:
                    print(f"Failed to send message to chat ID {chat_id}. Error: {e}")
            else:
                common_tags = set(tags) & set(user_tags)
                if common_tags:
                    try:
                        await bot.send_message(chat_id=chat_id, text=notification_text)
                        print(f"Message sent to chat ID {chat_id}")
                    except Exception as e:
                        print(f"Failed to send message to chat ID {chat_id}. Error: {e}")
                else:
                    print(f"User {chat_id} does not have any common tags with the notification.")

        # Update the CSV file to mark the notification as sent
        with open(NOTIFICATIONS_FILE, mode='r', encoding='utf-8') as file:
            reader = list(csv.DictReader(file))
        with open(NOTIFICATIONS_FILE, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = reader[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row.get('S. no.') == latest_notification.get('S. no.'):
                    row['telegram_notification_sent'] = '1'
                writer.writerow(row)

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_message_to_chat_ids())
