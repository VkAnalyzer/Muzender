# coding: utf-8
import logging
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram import bot
import telegram
import pickle
from rpc_client import RpcClient


MIN_NOVELTY_LEVEL = 1
MAX_NOVELTY_LEVEL = 150
DEFAULT_NOVELTY_LEVEL = 8


def start(bot, update):
    message = """Hi there, if you show me your vk.com profile, I will recommend you some cool music. Just drop the link."""
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


def give_recommendation(bot, update):
    recommender = RpcClient(host='queue', routing_key='rpc_recommendations')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='I need a minute to think about it')
    answer = recommender.call(user_preferences[update.message.chat_id])

    if answer == 'Sorry, you closed access to your music collection.':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=answer)
    else:
        if type(answer) is list:
            keyboard = []
            for artist in answer:
                artist = artist.lstrip()
                link = 'https://music.yandex.ru/search?text=' \
                       + artist.replace(' ', '%20') \
                       + '&type=artists'
                keyboard.append([telegram.InlineKeyboardButton(text=artist,
                                                               url=link)])

            markup = telegram.InlineKeyboardMarkup(keyboard)
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Check this out:",
                            reply_markup=markup,
                            )

            keyboard = [[telegram.KeyboardButton('more accurate'),
                         telegram.KeyboardButton('I like it!'),
                         telegram.KeyboardButton('less obvious')]]
            markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="your feedback is appreciated",
                            reply_markup=markup,
                            )


def echo(bot, update):
    sent = update.message.text.strip().lower()

    if 'vk.com/' in sent:
        vk_id = sent.split('/')[-1]
        logger.info('new user: {}'.format(vk_id))
        user_preferences[update.message.chat_id] = {'user_id': vk_id,
                                                    'novelty_level': DEFAULT_NOVELTY_LEVEL}
        give_recommendation(bot, update)
    elif update.message.chat_id in user_preferences.keys():
        if sent == 'more accurate':
            curr_novelty_level = user_preferences[update.message.chat_id]['novelty_level']
            user_preferences[update.message.chat_id]['novelty_level'] = max(int(curr_novelty_level / 2),
                                                                            MIN_NOVELTY_LEVEL)
            give_recommendation(bot, update)
        elif sent == 'less obvious':
            curr_novelty_level = user_preferences[update.message.chat_id]['novelty_level']
            user_preferences[update.message.chat_id]['novelty_level'] = min(int(curr_novelty_level * 2),
                                                                            MAX_NOVELTY_LEVEL)
            give_recommendation(bot, update)
        elif sent == 'i like it!':
            logger.info('user likes recommendation, details: {}'.format(user_preferences[update.message.chat_id]))
            bot.sendMessage(chat_id=update.message.chat_id, text='Thanks!')
        else:
            message = """Please, show me your vk.com profile, I will recommend you some cool music. Just drop the link."""
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
    else:
        message = """Please, show me your vk.com profile, I will recommend you some cool music. Just drop the link."""
        bot.sendMessage(chat_id=update.message.chat_id, text=message)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('tg bot')
    logger.info('Initialize tg bot')

    with open('token.pkl', 'rb') as f:
        token = pickle.load(f)

    user_preferences = {}
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
