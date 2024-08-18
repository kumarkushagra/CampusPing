# when called this function will send last message to the particular users.

import typing
from telegram import Bot
import asyncio

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
CHAT_IDS_FILE: typing.Final = 'chat_ids.txt'
NOTIFICATIONS_FILE: typing.Final = 'latest_notifications.txt'

async def send_message_to_chat_ids():
    bot = Bot(token=TOKEN)

    try:
        # Read the latest notification from the file
        with open(NOTIFICATIONS_FILE, "r") as file:
            notifications = file.read().strip().split('\n')
            if len(notifications) < 3:
                print("Insufficient notification data.")
                return
            # Extract the latest notification details
            summary = notifications[-3].strip()
            link = notifications[-2].strip()
            tags = notifications[-1].replace("Tags:", "").strip().lower().split(', ')
            notification_text = f"{summary}\n\n{link}\nTags: {', '.join(tags)}"
            print(f"Notification to send: {notification_text}")
            print(f"Tags of the notification: {tags}")

        # Read chat IDs and tags from the file
        chat_tags = {}
        with open(CHAT_IDS_FILE, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 3):  # Each chat ID entry spans 3 lines
                chat_id_line = lines[i].strip()
                tags_line = lines[i + 1].strip()
                
                if chat_id_line.startswith("Chat ID:"):
                    chat_id = chat_id_line.split(': ')[1].strip()
                    user_tags = tags_line.replace("Tags:", "").strip().lower().split(', ')
                    chat_tags[chat_id] = user_tags
                    print(f"User {chat_id} has tags: {user_tags}")

        # Send notification to users if they have any tag in common with the notification tags
        for chat_id, user_tags in chat_tags.items():
            common_tags = set(tags) & set(user_tags)
            if common_tags:
                try:
                    # Send the notification asynchronously
                    await bot.send_message(chat_id=chat_id, text=notification_text)
                    print(f"Message sent to chat ID {chat_id}: {notification_text}")
                except Exception as e:
                    print(f"Failed to send message to chat ID {chat_id}. Error: {e}")
            else:
                print(f"User {chat_id} does not have any common tags with the notification.")

    except FileNotFoundError:
        print("One or more files not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_message_to_chat_ids())
