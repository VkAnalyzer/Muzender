import logging
import os
import pickle

import numpy as np
import pandas as pd
import pika
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[sentry_logging]
)


def on_request(ch, method, props, body):
    body = pickle.loads(body)
    response = model.predict(body['user_id'], body['novelty_level'], body['user_music'])
    body['recommendations'] = response

    if props.reply_to and props.correlation_id:
        channel.basic_publish(exchange='',
                              routing_key=props.reply_to,
                              body=pickle.dumps(body),
                              properties=pika.BasicProperties(
                                  correlation_id=props.correlation_id),
                              )
        logger.info(f'Predictions sent to web_server')
    else:
        channel.basic_publish(exchange='',
                              routing_key='tg_bot',
                              body=pickle.dumps(body),
                              properties=pika.BasicProperties(),
                              )
        logger.info(f'Predictions sent to tg_bot')
    ch.basic_ack(delivery_tag=method.delivery_tag)


class Recommender(object):
    def __init__(self, n_recommendations=5, novelty_level=9):

        with open('../data/model_w2v.pkl', 'rb') as f:
            self.model = pickle.load(f)

        with open('../data/popularity.pkl', 'rb') as f:
            self.popularity = pickle.load(f)

        self.n_recommendations = n_recommendations
        self.novelty_level = novelty_level

    def _pick_random_items(self, scores, n):
        scores -= scores.min() - 1e-10
        scores /= np.sum(scores)
        chosen_items = np.random.choice(list(range(len(scores))), size=min(n, len(scores)), replace=False, p=scores)
        return chosen_items.astype(int).tolist()

    def predict(self, user_id, novelty_level=None, user_music='Nothing'):
        logger.info(f'New recommendation request  for user: {user_id}, novelty level: {novelty_level}')
        if novelty_level is None:
            novelty_level = self.novelty_level

        if user_music == 'Nothing':
            logger.info(f'User {user_id} closed access to music')
            return 'Sorry, you closed access to your music collection.'
        if len(user_music) == 0:
            logger.warning('Wrong user id or no music in collection.')
            return 'No such user or empty music collection.'

        artists = list(pd.DataFrame(user_music)['artist'])
        logger.info(f'Got {len(artists)} artists from parser.')

        recommendations = self.model.predict_output_word(artists, 200)
        if recommendations is None:
            logger.warning('user with empy recommendations')
            return 'It seems you like something too out of Earth.'

        recommendations = np.array(recommendations)
        scores = recommendations[:, 1].astype(float)
        # reweigh with reverse popularity
        popularity = np.array([self.popularity[artist] for artist in recommendations[:, 0]])
        scores *= (1 / popularity)

        recommendations = recommendations[self._pick_random_items(np.array(scores), 5), 0]
        logger.info(f'Recommendation: {recommendations}')
        return [str(a) for a in recommendations]


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('recommender')

    logger.info('Initialize model')
    model = Recommender()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='reco_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='reco_queue')

    logger.info('recommendation service ready')
    channel.start_consuming()
