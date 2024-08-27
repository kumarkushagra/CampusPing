import typing
from telegram import Bot
import asyncio
import pandas as pd
import ast  # For safely evaluating string representations of Python literals

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: typing.Final = os.getenv('TELEGRAM_API_TOKEN')
USER_DATA_FILE: typing.Final = 'user_data.csv'
NOTIFICATIONS_FILE: typing.Final = 'output.csv'

async def send_notifications():
    bot = Bot(token=TOKEN)

    try:
        # Read notifications from the CSV file using pandas
        notifications_df = pd.read_csv(NOTIFICATIONS_FILE)
        if notifications_df.empty:
            print("No notifications available.")
            return

        # Read user data from the CSV file using pandas
        user_data_df = pd.read_csv(USER_DATA_FILE)
        chat_tags = {}
        for _, row in user_data_df.iterrows():
            chat_id = str(row.get('Chat ID', '')).strip()
            user_tags = row.get('Tags', '').strip()
            if user_tags:
                user_tags = [tag.strip().lower() for tag in user_tags.split(',') if tag.strip()]
            else:
                user_tags = []
            chat_tags[chat_id] = user_tags

        # Iterate over notifications
        for idx, notification in notifications_df.iterrows():
            if notification['telegram_notification_sent'] == 0:  # Check if notification is not sent
                # Extract notification details
                summary = notification['LLM_summary'].strip()
                link = "https://www.imsnsit.org/imsnsit/notifications.php"
                tags = notification.get('tags', '').strip()

                # Process tags
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
                notifications_df.at[idx, 'telegram_notification_sent'] = 1

        # Save the updated DataFrame to the CSV file
        notifications_df.to_csv(NOTIFICATIONS_FILE, index=False)

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_notifications())
