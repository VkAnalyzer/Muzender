import logging
import pickle

import pika
import redisworks
import vk_api
from vk_api.audio import VkAudio


class VkParser(object):
    def __init__(self):
        with open('secret.pkl', mode='rb') as f:
            secret = pickle.load(f)
        self.vk_session = self.connect_vk(secret['login'], secret['password'])
        self.vk = self.vk_session.get_api()

    def connect_vk(self, login, password):
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

    @staticmethod
    def get_users_audio(session, vk_page):
        result = r[str(vk_page)]
        if result:
            logger.info('return from cache')
            return list(result)     # without list() pickle.dumps doesn't work

        vkaudio = VkAudio(session)
        all_audios = vkaudio.get(owner_id=vk_page)
        logger.info('got {} audios'.format(len(all_audios)))

        r[str(vk_page)] = all_audios

        return all_audios


def on_request(ch, method, props, body):
    body = pickle.loads(body)
    user_id = parser.get_user_id(link=body['user_id'])

    try:
        response = parser.get_users_audio(session=parser.vk_session, vk_page=user_id)
    except vk_api.AccessDenied:
        response = 'Nothing'
        logging.warning(f'access to {user_id} page denied')
    logger.info(f'parsed page of user {user_id}')

    body['user_music'] = response

    channel.basic_publish(exchange='',
                          routing_key='reco_queue',
                          properties=pika.BasicProperties(),
                          body=pickle.dumps(body),
                          )
    logger.info(f'send results to queue')
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('parser')

    logger.info('Initialize parser')
    parser = VkParser()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='user_id')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='user_id')

    r = redisworks.Root(host='redis')

    logger.info('parsing service ready')
    channel.start_consuming()
