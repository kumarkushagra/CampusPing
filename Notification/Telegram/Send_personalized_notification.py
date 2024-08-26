import pandas as pd
import re
import asyncio
from telegram import Bot
from telegram.error import TelegramError

# Your bot token
TOKEN = '7418556410:AAE4AIoE4aZAPQ0g5GcpFIVwMmf53DIx9ZU'
bot = Bot(token=TOKEN)

async def send_personalized_messages():
    # Read the CSV files
    user_data_df = pd.read_csv('user_data.csv')
    output_df = pd.read_csv('output.csv')

    # Get the extracted text of the last notice
    last_notice_text = output_df.iloc[-1]['extracted_text']
    print("Last notice text retrieved.")

    # Dictionary to keep track of which users have been messaged
    users_messaged = {}

    # Iterate over each user in user_data.csv
    for _, row in user_data_df.iterrows():
        name = row['Name']
        roll_number = row['Roll Number']
        chat_id = row['Chat ID']
        
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
        
        # Send a combined message if both name and roll number were found
        if name_found or roll_number_found:
            message = f"""Hello {name}, your {'name and roll number' if name_found and roll_number_found else 'name' if name_found else 'roll number'} was found in the latest notice. Please check it out!
Link: "https://www.imsnsit.org/imsnsit/notifications.php"
            """
            try:
                response = await bot.send_message(chat_id=chat_id, text=message)
                print(f"Message sent to {name}.")
                users_messaged[chat_id] = True
            except TelegramError as e:
                print(f"Failed to send message to {name}: {e}")

if __name__ == "__main__":
    # Run the asynchronous function
    asyncio.run(send_personalized_messages())
