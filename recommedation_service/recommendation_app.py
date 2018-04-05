import logging
import pika
import pickle
from scipy import sparse
import implicit
import pandas as pd
import numpy as np
from rpc_client import RpcClient


def on_request(ch, method, props, body):
    body = pickle.loads(body)
    response = model.predict(**body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=pickle.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


class Recommender(object):
    def __init__(self, n_recommendations=5, novelty_level=9):
        with open('data/dataset.pkl', 'rb') as f:
            self.dataset_s = pickle.load(f)

        with open('data/artist_names.pkl', 'rb') as f:
            self.artist_names = pickle.load(f)

        with open('data/model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        self.n_recommendations = n_recommendations
        self.novelty_level = novelty_level
        self.parser = None

    def predict(self, user_id, novelty_level=None):
        logger.info('New recommendation request  for user: {}, novelty level: {}'.format(user_id,
                                                                                         novelty_level))
        if novelty_level is None:
            novelty_level = self.novelty_level
        try:
            user_music = self.parser.call(user_id)
        except:
            self.parser = RpcClient(host='queue', routing_key='rpc_user_music')
            user_music = self.parser.call(user_id)

        if user_music is None:
            logger.info('User {} closed access to music'.format(user_id))
            return "Sorry, you closed access to your music collection."
        if len(user_music) == 0:
            logger.warning('Wrong user id or no music in collection.')
            return "No such user or empty music collection."

        artists = list(pd.DataFrame(user_music)['artist'])
        logger.info('Got {} artists from parser.'.format(len(artists)))
        user_items = np.zeros(len(self.artist_names))
        user_items[self.artist_names.isin(artists)] = 1
        logger.info('{} known artists.'.format(np.sum(user_items)))

        last_id = self.dataset_s.shape[0]  # last id+1
        recommendations = np.array(self.model.recommend(last_id,
                                                        sparse.vstack((self.dataset_s,
                                                                       sparse.csr_matrix(user_items))),
                                                        recalculate_user=True,
                                                        N=80
                                                        ))
        user_count = self.dataset_s.shape[0]
        popularity = []
        artists = recommendations[:, 0].astype(int)
        temp_dataset = self.dataset_s.tocsc()
        for artist in artists:
            popularity.append(temp_dataset[:, artist].count_nonzero() / user_count)

        artist_rating = (recommendations[:, 1]
                         * (1 - np.array(popularity) * novelty_level * 6))
        recommendation_indexes = artist_rating.argsort()[-self.n_recommendations:][::-1]

        recommendation = list(self.artist_names[recommendations[recommendation_indexes, 0]
                              .astype('int')])
        logger.info('Recommendation: {}'.format(recommendation))
        return recommendation


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('recommender')
    logger.info('Initialize model')
    model = Recommender()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_recommendations')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_recommendations')

    model.parser = RpcClient(host='queue', routing_key='rpc_user_music')

    logger.info('recommendation service ready')
    channel.start_consuming()
