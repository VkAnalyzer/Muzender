import logging
import os
import pickle
import time

import pika
import sentry_sdk
import vk_api
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[sentry_logging]
)


class VkCrawler():
    def __init__(self, level_count, max_friends=30, max_queue_len=100):
        self.level_count = level_count
        self.max_friends = max_friends
        self.max_queue_len = max_queue_len

        with open('../data/secret.pkl', mode='rb') as f:
            secret = pickle.load(f)
        vk_session = vk_api.VkApi(secret['login'], secret['password'])
        vk_session.auth()
        self.vk = vk_session.get_api()

        self.parsed_users = []

    def recursive_get_friends(self, vk_page, curr_level):
        if curr_level:
            try:
                result = self.vk.users.getFollowers(user_id=vk_page)['items'][:self.max_friends]
                result = [user for user in result if user not in self.parsed_users]
                for user in result:
                    channel.basic_publish(exchange='',
                                          routing_key='parser_queue',
                                          properties=pika.BasicProperties(),
                                          body=pickle.dumps({'vk_page': str(user)}),
                                          )
                    self.parsed_users.append(vk_page)

                    res = channel.queue_declare(queue='parser_queue', passive=True)
                    queue_length = res.method.message_count
                    while queue_length >= self.max_queue_len:
                        time.sleep(20)
                        res = channel.queue_declare(queue='parser_queue', passive=True)
                        queue_length = res.method.message_count

                for user in result:
                    self.recursive_get_friends(user, curr_level - 1)

            except vk_api.ApiError as e:
                logging.debug(f'user: {vk_page}, error: {e}')

    def start(self, user_zero):
        logging.info('starting crawler')
        self.recursive_get_friends(user_zero, self.level_count)
        logging.info(f'crawler stopped, {len(self.parsed_users)} users found')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('crawler')
    logger.propagate = False

    logger.info('Initialize crawler')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    crawler = VkCrawler(level_count=50,
                        max_friends=200,
                        max_queue_len=50,
                        )
    logger.info('crawling service ready')

    crawler.start(175381)
