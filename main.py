import logging
import time
from datetime import datetime
import pytz
from os import getenv
from dotenv import load_dotenv

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

import states

load_dotenv()
local_time = pytz.timezone(getenv('TIMEZONE'))
naive_dt = datetime.now()
local_dt = local_time.localize(naive_dt, is_dst=None)
start_date = local_dt.astimezone(pytz.utc)

def configure_log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def handler(update: Update, context: CallbackContext):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
    # Dont handle events in past
    if start_date > update.message.date:
        return 

    # if(update.message.chat_id != -250339505):
    #     return
    if not hasattr(context.bot, 'fsm'):
        context.bot.fsm = states.FSM(states.WaitCommand)
    
    context.bot.fsm.get_state().update(update, context)

def main():
    configure_log()
    updater = Updater(getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher
    # dispatcher.add_handler(CommandHandler('зарядить', start))
    dispatcher.add_handler(MessageHandler(Filters.text, handler))
    updater.start_polling()

if __name__ == "__main__":
    main()
