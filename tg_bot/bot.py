# coding: utf-8
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pickle
from recommedation_client import recommedation_client as rc


def echo(bot, update):
    sent = update.message.text.strip().lower()

    if 'vk.com/' in sent:
        sent = sent.split('/')[-1]
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='I need a minute to think about it')
        answer = recommender.call(sent)

        answer = (answer.replace('\\', '')
                        .replace(']', '')
                        .replace('[', '')
                        .replace('\'', '')
                        .split(','))

        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Check this out:')

        if type(answer) is list:
            for artist in answer:
                artist = artist.lstrip()

                message = (artist + '\n' +
                           'https://music.yandex.ru/search?text='
                           + artist.replace(' ', '%20')
                           + '&type=artists')
                bot.sendMessage(chat_id=update.message.chat_id, text=message)
    else:
        message = """Hi there, if you show me your vk.com profile, I will recommend you some cool music. Just drop the link."""
        bot.sendMessage(chat_id=update.message.chat_id, text=message)


if __name__ == '__main__':
    recommender = rc.RpcClient()
    with open('token.pkl', 'rb') as f:
        token = pickle.load(f)

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
