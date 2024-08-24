import typing
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import csv

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
BOT_USERNAME: typing.Final = '@NSUT_IMS_notification_bot'
CSV_FILE: typing.Final = 'output.csv'
USER_DATA_FILE: typing.Final = 'user_data.csv'

# Utility functions for CSV operations
def read_user_data():
    user_data = {}
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    chat_id = row['Chat ID']
                    name = row['Name']
                    tags = row['Tags']
                    roll_number = row['Roll Number']
                    user_data[chat_id] = {'Name': name, 'Tags': tags, 'Roll Number': roll_number}
        except Exception as e:
            print(f"Error reading user data: {e}")
    return user_data

def write_user_data(user_data):
    try:
        with open(USER_DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Chat ID", "Name", "Tags", "Roll Number"])
            writer.writeheader()
            for chat_id, data in user_data.items():
                writer.writerow({"Chat ID": chat_id, "Name": data['Name'], "Tags": data['Tags'], "Roll Number": data['Roll Number']})
    except Exception as e:
        print(f"Error writing user data: {e}")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Hello! How may I help you?

i) View latest notification by clicking /latest_notifications
ii) View all notifications by clicking /view_all_notifications
iii) Search any particular term in all the notifications by typing /search <term> 

This bot will send you automatic notifications in the future. You can select which type of notifications you would like to receive.
You can do this by selecting tags from /view_all_tags and then /edit_tags.''')

def read_notifications():
    notifications = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                notifications.append({
                    'LLM_summary': row['LLM_summary'],
                    'link_to_notice': "https://www.imsnsit.org/imsnsit/notifications.php",
                    'tags': row['tags'].split(', ')
                })
    except Exception as e:
        print(f"Error reading notifications: {e}")
    return notifications

async def latest_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notifications = read_notifications()
    
    # Get the latest 5 notifications
    latest_notifications = notifications[-5:]

    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification['LLM_summary']}\n\n{notification['link_to_notice']}\n**{', '.join(notification['tags'])}**\n" for i, notification in enumerate(latest_notifications))
    if not formatted_notifications:
        formatted_notifications = "No notifications available."
    
    await update.message.reply_text(formatted_notifications + "\n\n\nPress /view_all_notifications to see all previous notifications.")

async def search_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_term = ' '.join(context.args)
    if not search_term:
        await update.message.reply_text("Please provide a search term: /search <term>")
        return

    notifications = read_notifications()

    # Search notifications for the term
    matching_notifications = [notification for notification in notifications if search_term.lower() in notification['LLM_summary'].lower()]
    
    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification['LLM_summary']}\n\n{notification['link_to_notice']}\n**{', '.join(notification['tags'])}**\n" for i, notification in enumerate(matching_notifications))
    if not formatted_notifications:
        formatted_notifications = "No matching notifications found."
    
    await update.message.reply_text(formatted_notifications)

async def view_all_tags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                tags = set()
                for row in reader:
                    current_tags = row.get('tags', '').strip()
                    if current_tags:  # Check if there are any tags
                        # Remove unwanted characters and clean up tags
                        current_tags_list = [tag.strip().strip('[]').strip("'").strip() for tag in current_tags.split(",") if tag.strip()]
                        tags.update(current_tags_list)
                
                if tags:
                    unique_tags = sorted(tags)
                    # Create a formatted string with no unwanted characters
                    formatted_tags = "\n".join(unique_tags)
                    await update.message.reply_text(f"Unique Tags:\n{formatted_tags}")
                else:
                    await update.message.reply_text("No tags found.")
        except Exception as e:
            await update.message.reply_text(f"Error reading tags: {e}")
    else:
        await update.message.reply_text("No notifications file found.")

async def edit_tags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    new_tags = ' '.join(context.args)

    if not new_tags:
        await update.message.reply_text("Please provide tags to update: /edit_tags <tag1>,<tag2>....\nTo view all tags press /view_all_tags")
        return

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and tags
    if chat_id in user_data:
        user_data[chat_id]['Tags'] = new_tags
    else:
        user_data[chat_id] = {'Name': '', 'Tags': new_tags, 'Roll Number': ''}

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Tags updated to: {new_tags}")

async def show_tags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    user_data = read_user_data()

    if chat_id in user_data:
        tags = user_data[chat_id]['Tags']
        await update.message.reply_text(f"Your tags: {tags}")
    else:
        await update.message.reply_text("No tags found for your chat ID.")

async def enter_name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    name = ' '.join(context.args)

    if not name:
        await update.message.reply_text("Please provide your name: /enter_name <name>")
        return

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and name
    if chat_id in user_data:
        user_data[chat_id]['Name'] = name
    else:
        user_data[chat_id] = {'Name': name, 'Tags': '', 'Roll Number': ''}

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Name updated to: {name}")

async def enter_roll_number_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    roll_number = ' '.join(context.args)

    if not roll_number:
        await update.message.reply_text("Please provide your roll number: /enter_roll_number <roll_number>")
        return

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and roll number
    if chat_id in user_data:
        user_data[chat_id]['Roll Number'] = roll_number
    else:
        user_data[chat_id] = {'Name': '', 'Tags': '', 'Roll Number': roll_number}

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Roll number updated to: {roll_number}")

# Responses to updated via AI
def handle_responses(text: str) -> str:
    processed = text.lower()
    
    if 'hello' in processed:
        return "Hey there!"
    
    if 'how are you' in processed:
        return "I am good!"
    
    if 'send latest notification' in processed:
        return 'Type /latest_notifications to get the latest notifications'
    
    return "I don't understand. Type '/' to view actions."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    # Get all available tags
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                available_tags = set()
                for row in reader:
                    current_tags = row['tags'].strip()
                    current_tags_list = [tag.strip() for tag in current_tags.split(",")]
                    available_tags.update(current_tags_list)
        except Exception as e:
            await update.message.reply_text(f"Error reading tags: {e}")
            return
    else:
        available_tags = set()

    # Saving Chat ID in a CSV file
    chat_id = str(update.message.chat.id)
    user_data = read_user_data()
    
    if chat_id not in user_data:
        # Add new chat ID with tags
        user_data[chat_id] = {'Name': '', 'Tags': ', '.join(sorted(available_tags)), 'Roll Number': ''}
        write_user_data(user_data)
        print(f"Chat ID {chat_id} and tags added to the file.")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_responses(new_text)
        else:
            return
    else:
        response = handle_responses(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('latest_notifications', latest_notifications_command))
    app.add_handler(CommandHandler('search', search_notifications_command))
    app.add_handler(CommandHandler('view_all_tags', view_all_tags_command))
    app.add_handler(CommandHandler('edit_tags', edit_tags_command))
    app.add_handler(CommandHandler('show_my_tags', show_tags_command))
    app.add_handler(CommandHandler('enter_name', enter_name_command))
    app.add_handler(CommandHandler('enter_roll_number', enter_roll_number_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Log Errors
    app.add_error_handler(error)
    
    print("Polling...")
    app.run_polling(poll_interval=3)
