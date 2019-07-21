import logging
import os
import pickle

import pandas as pd
import pika
import redis
import sentry_sdk
import vk_api
from sentry_sdk.integrations.logging import LoggingIntegration
from vk_api.audio import VkAudio

USER_BATCH_SIZE = 100
CACHE_LIFETIME = 60 * 60 * 24 * 3  # 3 days in seconds
DATASET_PATH = '../data/vk_dataset.csv'

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[sentry_logging]
)


class VkParser(object):
    def __init__(self):
        with open('../data/secret.pkl', mode='rb') as f:
            secret = pickle.load(f)
        self.vk_session = self.connect_vk(secret['login'], secret['password'])
        self.vk = self.vk_session.get_api()
        self.parsed_users = []

    @staticmethod
    def connect_vk(login, password):
        session = vk_api.VkApi(login, password)
        try:
            session.auth()
            logger.info('authorized in VK')
        except vk_api.AuthError as error_msg:
            logger.critical('unathorized in vk with error: {}'.format(error_msg))
        return session

    def get_user_id(self, link):
        if 'vk.com/' in link:
            link = link.split('/')[-1]
        if link.replace('id', '').isdigit():
            user_id = link.replace('id', '')
        else:
            try:
                user_id = self.vk.utils.resolveScreenName(screen_name=link)['object_id']
            except TypeError:
                return None
        return int(user_id)

    def get_users_audio(self, session, vk_page):
        result = cache.get(str(vk_page))
        if result:
            logger.info('return from cache')
            return pickle.loads(result)

        vkaudio = VkAudio(session)
        all_audios = vkaudio.get(owner_id=vk_page)
        logger.info('got {} audios'.format(len(all_audios)))

        if all_audios:
            all_audios = pd.DataFrame(all_audios)
            all_audios['user_id'] = vk_page
            all_audios[['user_id', 'title', 'artist']].to_csv(DATASET_PATH, mode='a', index=None, header=None)

            all_audios = list(all_audios['artist'])[::-1]
            cache.setex(name=str(vk_page),
                        value=pickle._dumps(all_audios),
                        time=CACHE_LIFETIME)
        return all_audios


def on_request(ch, method, props, body):
    body = pickle.loads(body)
    vk_page = parser.get_user_id(link=body['vk_page'])

    try:
        response = parser.get_users_audio(session=parser.vk_session, vk_page=vk_page)
    except (vk_api.AccessDenied, AttributeError, TypeError) as e:
        response = 'Nothing'
        logging.warning(f'access to {vk_page} page denied')
    logger.info(f'parsed page of user {vk_page}')
    if ('chat_id' in body) or (props.reply_to and props.correlation_id):
        body['user_music'] = response

        channel.basic_publish(exchange='',
                              routing_key='reco_queue',
                              properties=pika.BasicProperties(
                                  reply_to=props.reply_to,
                                  correlation_id=props.correlation_id
                              ),
                              body=pickle.dumps(body),
                              )
        logger.info(f'send results to queue')
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('parser')
    logger.propagate = False

    logger.info('Initialize parser')
    parser = VkParser()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='parser_queue', arguments={'x-max-priority': 3})

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='parser_queue')

    cache = redis.Redis(host='redis')

    logger.info('parsing service ready')
    channel.start_consuming()
