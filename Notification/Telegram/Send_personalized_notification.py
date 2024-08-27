import pandas as pd
import re
import asyncio
from telegram import Bot
from telegram.error import TelegramError
import typing

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: typing.Final = os.getenv('TELEGRAM_API_TOKEN')
bot = Bot(token=TOKEN)

# File variables
USER_DATA_FILE = 'user_data.csv'
OUTPUT_FILE = 'output.csv'

async def send_personalized_messages():
    # Read the CSV files
    user_data_df = pd.read_csv(USER_DATA_FILE)
    output_df = pd.read_csv(OUTPUT_FILE)

    # Filter notices where telegram_notification_sent is 0
    unsent_notices = output_df[output_df['telegram_notification_sent'] == 0]

    # Debug line if no notice was retrieved
    if unsent_notices.empty:
        print("No unsent notices found.")
        return  # Exit the function if no unsent notices

    # Iterate over each notice where telegram_notification_sent is 0
    for _, notice_row in unsent_notices.iterrows():
        last_notice_text = notice_row['extracted_text']
        print("Last notice text retrieved.")

        # Flag to track if any messages were sent for this notice
        notification_sent = False

        # Iterate over each user in user_data.csv
        for _, user_row in user_data_df.iterrows():
            name = user_row['Name']
            roll_number = user_row['Roll Number']
            chat_id = user_row['Chat ID']
            
            # Convert name and roll_number to strings and handle NaN values
            name = str(name) if pd.notna(name) else ''
            roll_number = str(roll_number) if pd.notna(roll_number) else ''

            # Initialize flags for sending messages
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
            
            # Send a combined message if either name or roll number were found
            if name_found or roll_number_found:
                message = f"""Hello {name}, your {'name and roll number' if name_found and roll_number_found else 'name' if name_found else 'roll number'} was found in the latest notice. Please check it out!
Link: "https://www.imsnsit.org/imsnsit/notifications.php"
                """
                try:
                    await bot.send_message(chat_id=chat_id, text=message)
                    print(f"Message sent to {name}.")
                    notification_sent = True  # Mark that a message was sent
                except TelegramError as e:
                    print(f"Failed to send message to {name}: {e}")

        # If no messages were sent for this notice, print the debug line
        if not notification_sent:
            print("No notifications were sent for this notice.")

if __name__ == "__main__":
    # Run the asynchronous function
    asyncio.run(send_personalized_messages())
