# coding: utf-8
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pickle



def echo(bot, update):
    sent = update.message.text.strip().lower()

    if sent in ['2', '4']:
        answer = 'even'
    elif sent in ['1', '3']:
        answer = 'odd'
    else:
        answer = 'I dont know this number'

    bot.sendMessage(chat_id=update.message.chat_id, text=answer)


if __name__ == '__main__':
    with open('token.pkl', 'rb') as f:
        token = pickle.load(f)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
