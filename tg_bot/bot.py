# coding: utf-8
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pickle
from recommedation_client import recommedation_client as rc


def echo(bot, update):
    sent = update.message.text.strip().lower()

    if 'vk.com/' in sent:
        sent = sent.split('/')[-1]
    if sent.replace('id', '').isdigit():
        sent = sent.replace('id', '')
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='I need a minute to think about it')
        answer = recommender.call(sent)
    else:
        answer = """Hi there, if you show me your vk.com profile, I will recommend you some cool music. Just drop the link."""

    bot.sendMessage(chat_id=update.message.chat_id, text=answer)


if __name__ == '__main__':
    recommender = rc.RpcClient()
    with open('token.pkl', 'rb') as f:
        token = pickle.load(f)

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
