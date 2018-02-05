import collections
import pickle
import pika
import time
import bs4
import vk_api
from vk_api.audio import VkAudio


# TODO: собрать все в класс
def connect_vk(login, password):
    session = vk_api.VkApi(login, password)

    try:
        session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
    return session


def get_user_id(link):
    if 'vk.com/' in link:
        link = link.split('/')[-1]
    if link.replace('id', '').isdigit():
        user_id = link.replace('id', '')
    else:
        user_id = vk.utils.resolveScreenName(screen_name=link)['object_id']

    return int(user_id)


def get_users_audio(session, vk_page):
    vkaudio = VkAudio(session)

    all_audios = []
    offset = 0

    while True:
        audios = vkaudio.get(owner_id=vk_page, offset=offset)
        all_audios.append(audios)
        offset += len(audios)

        if not audios:
            break

    all_audios = sum(all_audios, [])
    return all_audios


def on_request(ch, method, props, body):

    user_id = get_user_id(body.decode("utf-8"))

    try:
        response = get_users_audio(vk_session, user_id)
    except vk_api.AccessDenied:
        response = None
    print("parsed page of user", user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=pickle.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    with open('secret.pkl', mode='rb') as f:
        secret = pickle.load(f)
    vk_session = connect_vk(secret['login'], secret['password'])
    vk = vk_session.get_api()

    time.sleep(15)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_user_music')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_user_music')

    print("parsing service ready")
    channel.start_consuming()
