import logging
import os
import pickle
from threading import Thread

import pika
import sentry_sdk
import telegram
from sentry_sdk.integrations.logging import LoggingIntegration
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext import Updater

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[sentry_logging]
)

MIN_POPULARITY_LEVEL = 4
MAX_POPULARITY_LEVEL = 10
DEFAULT_POPULARITY_LEVEL = 7
TG_BOT_PRIORITY = 2  # message priority inn queue higher is better


def start(bot, update):
    message = '''
    Привет, я робот, но я немного понимаю в музыке.
    Cбрось мне ссылку на свой профиль Вконтакте, а я порекомендую тебе что-нибудь новенькое.
    '''
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


def request_recommendations(body):
    channel.basic_publish(exchange='',
                          routing_key='user_id',
                          body=pickle.dumps(body),
                          properties=pika.BasicProperties(priority=TG_BOT_PRIORITY),
                          )
    logger.info(f'send recommendation request for user {body["user_id"]} with popularity_level \
                {body["popularity_level"]}')


def on_request(ch, method, props, body):
    body = pickle.loads(body)
    answer = body['recommendations']
    bot = body['bot']

    if answer == 'Прости, но, похоже, ты закрыл доступ к своей музыке.':
        bot.sendMessage(chat_id=body['chat_id'],
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
            bot.sendMessage(chat_id=body['chat_id'],
                            text='Думаю, это тебе может понравиться:',
                            reply_markup=markup,
                            )

            keyboard = [[telegram.KeyboardButton('менее популярное'),
                         telegram.KeyboardButton('более популярное')],
                        [telegram.KeyboardButton('мое последнее'),
                         telegram.KeyboardButton('общее')],
                        [telegram.KeyboardButton('класс, мне понравилось!')],
                        ]
            markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            bot.sendMessage(chat_id=body['chat_id'],
                            text='Что думаешь?',
                            reply_markup=markup,
                            )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def echo(bot, update):
    sent = update.message.text.strip().lower()

    body = {'bot': bot,
            'chat_id': update.message.chat_id
            }

    if 'vk.com/' in sent:
        vk_id = sent.split('/')[-1]
        logger.info('new user: {}'.format(vk_id))
        user_preferences[update.message.chat_id] = {'user_id': vk_id}
        body.update(user_preferences[update.message.chat_id])
        request_recommendations(body)
    elif update.message.chat_id in user_preferences.keys():
        if sent == 'более популярное':
            curr_popularity_level = user_preferences[update.message.chat_id].get('popularity_level',
                                                                                 DEFAULT_POPULARITY_LEVEL)
            user_preferences[update.message.chat_id]['popularity_level'] = min(curr_popularity_level + 1,
                                                                               MAX_POPULARITY_LEVEL)
            body.update(user_preferences[update.message.chat_id])
            request_recommendations(body)
        elif sent == 'менее популярное':
            curr_popularity_level = user_preferences[update.message.chat_id].get('popularity_level',
                                                                                 DEFAULT_POPULARITY_LEVEL)
            user_preferences[update.message.chat_id]['popularity_level'] = max(curr_popularity_level - 1,
                                                                               MIN_POPULARITY_LEVEL)
            body.update(user_preferences[update.message.chat_id])
            request_recommendations(body)
        elif sent == 'класс!':
            logger.info('user likes recommendation, details: {}'.format(user_preferences[update.message.chat_id]))
            bot.sendMessage(chat_id=update.message.chat_id, text='Thanks!')
        else:
            message = 'Сбрасывай ссылку на свою страницу vk, а я порекомендую музыку.'
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
    else:
        message = 'Просто сбось ссылку на свой vk.'
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
    Thread(target=updater.start_polling())

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
        channel = connection.channel()
        channel.queue_declare(queue='tg_bot')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue='tg_bot')
        channel.start_consuming()
    except:
        # close all threads if connection is lost
        os._exit(1)
