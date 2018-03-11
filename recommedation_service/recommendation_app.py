import pika
import pickle
from scipy import sparse
import implicit
import pandas as pd
import numpy as np
from rpc_client import RpcClient


def on_request(ch, method, props, body):
    body = pickle.loads(body)
    # TODO: make body dictionary and pass dict to function
    if len(body) == 2:
        response = model.predict(user_id=body[0], novely_level=body[1])
    else:
        response = model.predict(body[0])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id
                                                     =props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


class Recommender(object):
    def __init__(self, n_recommendations=5, novely_level=9):
        with open('data/dataset.pkl', 'rb') as f:
            self.dataset_s = pickle.load(f)

        with open('data/artist_names.pkl', 'rb') as f:
            self.artist_names = pickle.load(f)

        with open('data/model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        self.n_recommendations = n_recommendations
        self.novely_level = novely_level

    def predict(self, user_id, novely_level=None):
        if novely_level is None:
            novely_level = self.novely_level
        response = parser.call(user_id)
        user_music = user_music = pickle.loads(response)

        if user_music is None:
            return "Sorry, you closed access to your music collection."
        if len(user_music) == 0:
            return "No such user or empty music collection."

        artists = list(pd.DataFrame(user_music)['artist'])
        user_items = np.zeros(len(self.artist_names))
        user_items[self.artist_names.isin(artists)] = 1

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
                         * (1 - np.array(popularity) * novely_level * 6))
        recommendation_indexes = artist_rating.argsort()[-self.n_recommendations:][::-1]
        return list(self.artist_names[recommendations[recommendation_indexes, 0]
                    .astype('int')])


if __name__ == '__main__':
    model = Recommender()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_recommendations')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_recommendations')

    parser = RpcClient(host='queue', routing_key='rpc_user_music')

    print("recommendation service ready")
    channel.start_consuming()
