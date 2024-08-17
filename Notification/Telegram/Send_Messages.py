import typing
from telegram import Bot
import asyncio
#from LLM_api import LLM_contact

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
CHAT_IDS_FILE: typing.Final = 'chat_ids.txt'
#new_notification = LLM_contact.summary

async def send_message_to_chat_ids():
    bot = Bot(token=TOKEN)

    try:
        with open(CHAT_IDS_FILE, "r") as file:
            chat_ids = [line.split(': ')[1].strip() for line in file.readlines() if line.strip()]

        for chat_id in chat_ids:
            try:
                # Send message asynchronously
                await bot.send_message(chat_id=chat_id, text="new_notification") #Yaha update hoga
                print(f"Message sent to chat ID {chat_id}")
            except Exception as e:
                print(f"Failed to send message to chat ID {chat_id}. Error: {e}")

    except FileNotFoundError:
        print(f"File {CHAT_IDS_FILE} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Run the async function using asyncio
    asyncio.run(send_message_to_chat_ids())
