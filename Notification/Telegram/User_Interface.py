import typing
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from Utility_functions import *

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: typing.Final = os.getenv('TELEGRAM_API_TOKEN')
BOT_USERNAME: typing.Final = '@NSUT_IMS_notification_bot'
CSV_FILE: typing.Final = 'output.csv'
USER_DATA_FILE: typing.Final = 'user_data.csv'

# Define the states for ConversationHandler
ENTER_NAME, ENTER_ROLL_NUMBER, EDIT_TAGS, SEARCH,ENTER_EMAIL,ENTER_PHONE_NUMBER = range(6)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Hello! How may I help you?
                                    
You can give us your Name and Roll no, and this bot will search your Name and Roll Number in the latest notices and notify you if found.

This bot also sends you summary of all the latest notices released, you can edit your tags to only receive relevant notifications.
                                    
/enter_name : Enter your name
/enter_roll_number : Enter your Roll number
/enter_email : Enter your Email to get notified via Email too
/enter_phone_number : Enter your Number to get notified via SMS too
/latest_notifications : View 5 latest notification
/search : Search any particular term in all the notifications
/view_all_tags : See all the tags
/enter_tags : Edit your tags 
/show_my_data : Shows Your user data
                                    ''')

async def latest_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notifications = read_notifications()
    
    # Get the latest 5 notifications
    latest_notifications = notifications[-5:][::-1]

    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(
        f"{i+1}. {notification['LLM_summary']}\n\n{notification['link_to_notice']}\n**{', '.join(notification['tags'])}**\n"
        for i, notification in enumerate(latest_notifications)
    )
    if not formatted_notifications:
        formatted_notifications = "No notifications available."
    
    await update.message.reply_text(formatted_notifications)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter the search term below:")
    return SEARCH

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_term = update.message.text
    notifications = read_notifications()

    # Search notifications for the term
    matching_notifications = [
        notification for notification in notifications
        if search_term.lower() in notification['LLM_summary'].lower()
    ]
    
    # Format notifications with indexing and new lines
    formatted_notifications = "\n\n".join(
        f"{i+1}. {notification['LLM_summary']}\n\n{notification['link_to_notice']}\n**{', '.join(notification['tags'])}**\n"
        for i, notification in enumerate(matching_notifications)
    )
    if not formatted_notifications:
        formatted_notifications = "No matching notifications found."
    
    await update.message.reply_text(formatted_notifications)

    return ConversationHandler.END

async def view_all_tags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tags = read_tags_from_csv()
    if tags:
        unique_tags = sorted(tags)
        formatted_tags = "\n".join(unique_tags)
        await update.message.reply_text(f"Unique Tags:\n{formatted_tags}")
    else:
        await update.message.reply_text("No tags found.")

async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your full name below:")
    return ENTER_NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.message.chat.id)
    name = update.message.text

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and name
    user_data[chat_id] = user_data.get(chat_id, {'Name': '', 'Tags': '', 'Roll Number': ''})
    user_data[chat_id]['Name'] = name

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Name updated to: {name}")

    return ConversationHandler.END

async def enter_roll_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your roll number below:")
    return ENTER_ROLL_NUMBER

async def handle_roll_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.message.chat.id)
    roll_number = update.message.text

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and roll number
    user_data[chat_id] = user_data.get(chat_id, {'Name': '', 'Tags': '', 'Roll Number': ''})
    user_data[chat_id]['Roll Number'] = roll_number

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Roll number updated to: {roll_number}")

    return ConversationHandler.END

async def enter_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your email address below:")
    return ENTER_EMAIL

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.message.chat.id)
    email = update.message.text

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and email
    user_data[chat_id] = user_data.get(chat_id, {'Name': '', 'Tags': '', 'Roll Number': '', 'Email': ''})
    user_data[chat_id]['Email'] = email

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Email updated to: {email}")

    return ConversationHandler.END

async def edit_tags(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("""Please enter the new tags below (comma-separated):
To view all tags press /view_all_tags
                                    """)
    return EDIT_TAGS

async def handle_tags(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.message.chat.id)
    new_tags = update.message.text

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and tags
    user_data[chat_id] = user_data.get(chat_id, {'Name': '', 'Tags': '', 'Roll Number': ''})
    user_data[chat_id]['Tags'] = new_tags

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Tags updated to: {new_tags}")

    return ConversationHandler.END

async def enter_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your phone number below:")
    return ENTER_PHONE_NUMBER

async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.message.chat.id)
    phone_number = update.message.text

    # Read existing user data
    user_data = read_user_data()

    # Update or add the chat ID and phone number
    user_data[chat_id] = user_data.get(chat_id, {'Name': '', 'Tags': '', 'Roll Number': '', 'Email': '', 'Phone Number': ''})
    user_data[chat_id]['Phone Number'] = phone_number

    # Write updated user data to file
    write_user_data(user_data)

    await update.message.reply_text(f"Phone number updated to: {phone_number}")

    return ConversationHandler.END

async def show_my_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    user_data = read_user_data()

    if chat_id in user_data:
        name = user_data[chat_id].get('Name', 'Not provided')
        roll_number = user_data[chat_id].get('Roll Number', 'Not provided')
        tags = user_data[chat_id].get('Tags', 'No tags assigned')
        email = user_data[chat_id].get('Email', 'Not provided')
        phone_number = user_data[chat_id].get('Phone Number', 'Not provided')
        
        await update.message.reply_text(
            f"Here is your data:\n\n"
            f"Name: {name}\n"
            f"Roll Number: {roll_number}\n"
            f"Email: {email}\n"
            f"Phone Number: {phone_number}\n"
            f"Tags: {tags}"
        )
    else:
        await update.message.reply_text("No data found for your chat ID. Please enter your name and roll number using the respective commands.")

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
    available_tags = read_tags_from_csv()

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

    # Define the conversation handlers
    enter_name_handler = ConversationHandler(
        entry_points=[CommandHandler('enter_name', enter_name)],
        states={
            ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)]
        },
        fallbacks=[]
    )

    enter_roll_number_handler = ConversationHandler(
        entry_points=[CommandHandler('enter_roll_number', enter_roll_number)],
        states={
            ENTER_ROLL_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roll_number)]
        },
        fallbacks=[]
    )

    enter_email_handler = ConversationHandler(
        entry_points=[CommandHandler('enter_email', enter_email)],
        states={
            ENTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)]
        },
        fallbacks=[]
    )

    enter_phone_number_handler = ConversationHandler(
        entry_points=[CommandHandler('enter_phone_number', enter_phone_number)],
        states={
            ENTER_PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_number)]
        },
        fallbacks=[]
    )

    edit_tags_handler = ConversationHandler(
        entry_points=[CommandHandler('enter_tags', edit_tags)],
        states={
            EDIT_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tags)]
        },
        fallbacks=[]
    )

    search_handler = ConversationHandler(
        entry_points=[CommandHandler('search', search_command)],
        states={
            SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search)]
        },
        fallbacks=[]
    )

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('latest_notifications', latest_notifications_command))
    app.add_handler(CommandHandler('view_all_tags', view_all_tags_command))
    app.add_handler(CommandHandler('show_my_data', show_my_data_command))
    
    # Add conversation handlers
    app.add_handler(enter_name_handler)
    app.add_handler(enter_roll_number_handler)
    app.add_handler(edit_tags_handler)
    app.add_handler(search_handler)
    app.add_handler(enter_email_handler)
    app.add_handler(enter_phone_number_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Log Errors
    app.add_error_handler(error)
    
    print("Polling...")
    app.run_polling(poll_interval=3)
