import typing
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
BOT_USERNAME: typing.Final = '@NSUT_IMS_notification_bot'
NOTIFICATIONS_FILE: typing.Final = 'latest_notifications.txt'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! How may I help you?')

def read_notifications(file_path: str):
    notifications = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            # Group lines into chunks of three
            for i in range(0, len(lines), 4):  # 4 because there is an empty line between each notification
                if i + 2 < len(lines):  # Ensure there are at least 3 lines for a notification
                    summary = lines[i].strip()
                    link = lines[i + 1].strip()
                    tags = lines[i + 2].strip()
                    notifications.append(f"{summary}\n\n {link} \n **{tags}**\n")
    return notifications[::-1]  # Reverse the list to show notifications bottom to top

async def latest_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notifications = read_notifications(NOTIFICATIONS_FILE)
    
    # Get the latest 5 notifications from the bottom to top
    latest_notifications = notifications[:5]  # Get from the start because it's reversed

    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification}" for i, notification in enumerate(latest_notifications))
    if not formatted_notifications:
        formatted_notifications = "No notifications available."
    
    await update.message.reply_text(formatted_notifications + "\n\n\nType /view_all_notifications to see all previous notifications.")

async def view_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notifications = read_notifications(NOTIFICATIONS_FILE)

    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification}" for i, notification in enumerate(notifications))
    if not formatted_notifications:
        formatted_notifications = "No notifications available."
    
    await update.message.reply_text(formatted_notifications)

async def search_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_term = ' '.join(context.args)  # Get the search term from the command arguments
    if not search_term:
        await update.message.reply_text("Please provide a search term: /search <term>")
        return

    notifications = read_notifications(NOTIFICATIONS_FILE)

    # Search notifications for the term
    matching_notifications = [notification for notification in notifications if search_term.lower() in notification.lower()]
    
    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification}" for i, notification in enumerate(matching_notifications))
    if not formatted_notifications:
        formatted_notifications = "No matching notifications found."
    
    await update.message.reply_text(formatted_notifications)

async def view_all_tags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, "r") as file:
            lines = file.readlines()
            tags = set()
            for i in range(2, len(lines), 4):  # Start from the third line of each notification
                if i < len(lines):
                    current_tags = lines[i].strip().replace("Tags:", "").strip()  # Remove "Tags:" prefix
                    current_tags_list = [tag.strip().lower() for tag in current_tags.split(",")]  # Normalize to lowercase
                    tags.update(current_tags_list)
            if tags:
                unique_tags = sorted(tags, key=str.lower)
                await update.message.reply_text("Unique Tags:\n" + "\n".join(unique_tags))
            else:
                await update.message.reply_text("No tags found.")
    else:
        await update.message.reply_text("No notifications file found.")
        

# Responses
def handle_responses(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return "Hey there!"
    
    if 'how are you' in processed:
        return "I am good!"
    
    if 'send latest notification' in processed:
        return 'type /notification to get all notifications'
    
    return "I don't understand, type '/' to view actions"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    # Get all available tags
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, "r") as file:
            lines = file.readlines()
            available_tags = set()
            for i in range(2, len(lines), 4):  # Start from the third line of each notification
                if i < len(lines):
                    current_tags = lines[i].strip().replace("Tags:", "").strip()
                    current_tags_list = [tag.strip() for tag in current_tags.split(",")]
                    available_tags.update(current_tags_list)
    else:
        available_tags = set()

    # Saving Chat ID in a text file
    chat_id = update.message.chat.id
    try:
        # Checking if user ID is already saved
        with open("chat_ids.txt", "r") as file:
            existing_chat_ids = file.read()
        
        if f"Chat ID: {chat_id}\n" in existing_chat_ids:
            print(f"Chat ID {chat_id} already exists in the file.")
        else:
            with open("chat_ids.txt", "a") as file:
                file.write(f"Chat ID: {chat_id}\n")
                file.write(f"Tags: {', '.join(sorted(available_tags))}\n\n")
            print(f"Chat ID {chat_id} and tags added to the file.")
    
    except FileNotFoundError:
        # File does not exist, so create it and add the chat ID
        with open("chat_ids.txt", "a") as file:
            file.write(f"Chat ID: {chat_id}\n")
            file.write(f"Tags: {', '.join(sorted(available_tags))}\n\n")
        print(f"Chat ID {chat_id} and tags added to the new file.")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_responses(new_text)
        else:
            return
    else:
        response: str = handle_responses(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('latest_notifications', latest_notifications_command))
    app.add_handler(CommandHandler('view_all_notifications', view_all_command))
    app.add_handler(CommandHandler('search', search_notifications_command))
    app.add_handler(CommandHandler('view_all_tags', view_all_tags_command))  # Added view_all_tags command
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print('Polling... ')
    app.run_polling(poll_interval=3)
