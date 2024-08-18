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

async def latest_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Read the notifications from the file
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, "r") as file:
            notifications = file.read().strip().split('\n')
    else:
        notifications = []

    # Get the latest 5 notifications
    latest_notifications = notifications[-5:] if notifications else []

    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification}" for i, notification in enumerate(latest_notifications))
    if not formatted_notifications:
        formatted_notifications = "No notifications available."
    
    await update.message.reply_text(formatted_notifications + "\n\n\nType /view_all_notifications to see all previous notifications.")

async def view_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Read the notifications from the file
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, "r") as file:
            notifications = file.read().strip().split('\n')
    else:
        notifications = []

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

    # Read the notifications from the file
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, "r") as file:
            notifications = file.read().strip().split('\n')
    else:
        notifications = []

    # Search notifications for the term
    matching_notifications = [notification for notification in notifications if search_term.lower() in notification.lower()]
    
    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(f"{i+1}. {notification}" for i, notification in enumerate(matching_notifications))
    if not formatted_notifications:
        formatted_notifications = "No matching notifications found."
    
    await update.message.reply_text(formatted_notifications)

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

    # Saving Chat ID in a text file
    chat_id = update.message.chat.id
    try:
        # Checking if user ID is already saved
        with open("chat_ids.txt", "r") as file:
            existing_chat_ids = file.readlines()
        
        if any(f"Chat ID: {chat_id}\n" in line for line in existing_chat_ids):
            print(f"Chat ID {chat_id} already exists in the file.")
        else:
            with open("chat_ids.txt", "a") as file:
                file.write(f"Chat ID: {chat_id}\n")
            print(f"Chat ID {chat_id} added to the file.")
    
    except FileNotFoundError:
        # File does not exist, so create it and add the chat ID
        with open("chat_ids.txt", "a") as file:
            file.write(f"Chat ID: {chat_id}\n")
        print(f"Chat ID {chat_id} added to the new file.")

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
    # Comment out or remove the help command
    # app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('latest_notifications', latest_notifications_command))
    app.add_handler(CommandHandler('view_all_notifications', view_all_command))
    app.add_handler(CommandHandler('search', search_notifications_command))  # Added search command
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print('Polling... ')
    app.run_polling(poll_interval=3)
