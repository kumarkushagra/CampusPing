import typing
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#from LLM_api import LLM_contact

TOKEN: typing.Final = '7418556410:AAGQ1Rz01PRCa8Z0qtHV33_twEspGY92rd0'
BOT_USERNAME: typing.Final = '@NSUT_IMS_notification_bot'


#Fetch Notification
# abhi chal nahi raha yeh 
# new_notification = 'Here is a summary of the latest notification: \n'+ LLM_contact.summary

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! How may I help you?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('......')


async def latest_notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('new_notification') #yaha change krna


#Responses
def handle_responses (text: str) -> str:
    processed : str = text.lower()
    
    if 'hello' in processed:
        return "Hey there!"
    
    if 'how are you' in processed:
        return "I am good!"
    
    if 'Send latest notification' in processed:
        return 'new_notification' # yaha change krna
    
    return "I dont understand"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print(f'User({update.message.chat.id}) in{message_type}: "text"')

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
            response: str =handle_responses(new_text)
        else:
            return
    else:
        response: str = handle_responses(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error (update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')
     

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('notification', latest_notifications_command))
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Error
    app.add_error_handler(error)

    #Polls the bot
    print('Polling... ')
    app.run_polling(poll_interval=3)
