import typing
from telegram import Bot
import asyncio

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
CHAT_IDS_FILE: typing.Final = 'chat_ids.txt'
NOTIFICATIONS_FILE: typing.Final = 'latest_notifications.txt'

async def send_message_to_chat_ids():
    bot = Bot(token=TOKEN)

    try:
        with open(CHAT_IDS_FILE, "r") as file:
            chat_ids = [line.split(': ')[1].strip() for line in file.readlines() if line.strip()]

        # Read the last notification from the notifications file
        with open(NOTIFICATIONS_FILE, "r") as file:
            notifications = file.read().strip().split('\n')
            if notifications:
                last_notification = notifications[-1]
            else:
                print("No notifications available.")
                return

        for chat_id in chat_ids:
            try:
                # Send the last notification asynchronously
                await bot.send_message(chat_id=chat_id, text=last_notification)
                print(f"Message sent to chat ID {chat_id}: {last_notification}")
            except Exception as e:
                print(f"Failed to send message to chat ID {chat_id}. Error: {e}")

    except FileNotFoundError:
        print(f"One or more files not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_message_to_chat_ids())
