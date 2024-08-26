import pandas as pd
import time
import asyncio

from Fetch_new_notices.create_csv import update_CSV
from Fetch_new_notices.create_csv_and_append_row import *
from Fetch_new_notices.is_target_tr import *

from Fetch_new_notices.create_csv import main as fetch_notices_main
from summary_generator_pipeline import process_notices

from Notification.Telegram.Send_Messages import *
from Notification.Telegram.Send_personalized_notification import *


def check_for_new_notices():
    try:
        # Read the existing CSV file
        df = pd.read_csv("database/notice.csv")
    except FileNotFoundError:
        # If the file doesn't exist, consider it as having no notices
        return False
    
    # Check if there are any unprocessed notices
    new_notices = df[df['Processed_status'] == 0]
    
    # If there are new notices
    return not new_notices.empty

def main():
    while True:
        # Run the fetch_notices_main function to update the CSV
        fetch_notices_main()
        
        # Wait for a few seconds to ensure the CSV is updated
        time.sleep(5)
        
        # Check if new notices are detected
        if check_for_new_notices():
            # Run the summary generator pipeline if new notices are found
            process_notices()
            asyncio.run(send_personalized_messages())
            asyncio.run(send_message_to_chat_ids())
        
        # Wait for 20 minutes before fetching new notices again
        time.sleep(1200)  # 1200 seconds = 20 minutes

if __name__ == "__main__":
    print("Deployment successful")
    main()
