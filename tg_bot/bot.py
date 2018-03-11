# coding: utf-8
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram import bot
import telegram
import pickle
from recommedation_client import recommedation_client as rc


MIN_NOVELTY_LEVEL = 1
MAX_NOVELTY_LEVEL = 150

def start(bot, update):
    message = """Hi there, if you show me your vk.com profile, I will recommend you some cool music. Just drop the link."""
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=message,
                    )


def give_recommendation(sent, curr_novelty_level, bot, update):
    if sent is None:
        try:
            vk_id = user_preferences[update.message.chat_id]['vk_id']
        except KeyError:
            bot.sendMessage(chat_id=update.message.chat_id, text='Good, now give me the link to your vk.com page')
            return
    else:
        vk_id = sent.split('/')[-1]
        user_preferences[update.message.chat_id]['vk_id'] = vk_id
    recommender = rc.RpcClient()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='I need a minute to think about it')
    answer = recommender.call([vk_id, curr_novelty_level])

    if answer == 'Sorry, you closed access to your music collection.':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=answer)
    else:
        answer = (answer.replace('\\', '')
                  .replace(']', '')
                  .replace('[', '')
                  .replace('\'', '')
                  .split(','))

        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Check this out:')

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
    try:
        curr_novelty_level = user_preferences[update.message.chat_id]['novelty_level']
    except:
        user_preferences[update.message.chat_id] = {'novelty_level': 9}
        curr_novelty_level = 9
        # TODO: set default novelty level somewhere

    sent = update.message.text.strip().lower()

    if 'vk.com/' in sent:
        give_recommendation(sent, curr_novelty_level, bot, update)
    elif sent == 'more accurate':
        curr_novelty_level = user_preferences[update.message.chat_id]['novelty_level']
        user_preferences[update.message.chat_id]['novelty_level'] = max(int(curr_novelty_level / 2),
                                                                        MIN_NOVELTY_LEVEL)
        give_recommendation(None, curr_novelty_level, bot, update)
        # TODO: set default novelty level
    elif sent == 'less obvious':
        curr_novelty_level = user_preferences[update.message.chat_id]['novelty_level']
        user_preferences[update.message.chat_id]['novelty_level'] = min(int(curr_novelty_level * 2),
                                                                        MAX_NOVELTY_LEVEL)
        give_recommendation(None, curr_novelty_level, bot, update)
    elif sent == 'i like it!':
        bot.sendMessage(chat_id=update.message.chat_id, text='Thanks!')
    else:
        message = """Please, show me your vk.com profile, I will recommend you some cool music. Just drop the link."""
        bot.sendMessage(chat_id=update.message.chat_id, text=message)
        # TODO: log nice feedback


if __name__ == '__main__':
    with open('token.pkl', 'rb') as f:
        token = pickle.load(f)

    user_preferences = {}
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
