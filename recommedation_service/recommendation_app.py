import pika
import uuid
import pickle
from scipy import sparse
import implicit
import pandas as pd
import numpy as np
from rpc_client import RpcClient


def predict(user_id):
    n_recommendations = 5
    novely_level = 9

    response = parser.call(user_id)
    user_music = pickle.loads(response)

    if user_music is None:
        return "Sorry, you closed access to your music collection."
    if len(user_music) == 0:
        return "No such user or empty music collection."

    artists = list(pd.DataFrame(user_music)['artist'])
    user_items = np.zeros(len(artist_names))
    user_items[artist_names.isin(artists)] = 1

    last_id = dataset_s.shape[0]  # last id+1
    recommendations = np.array(model.recommend(last_id,
                                               sparse.vstack((dataset_s,
                                                              sparse.csr_matrix(user_items))),
                                               recalculate_user=True,
                                               N=80
                                               ))
    user_count = dataset_s.shape[0]
    popularity = []
    artists = recommendations[:, 0].astype(int)
    temp_dataset = dataset_s.tocsc()
    for artist in artists:
        popularity.append(temp_dataset[:, artist].count_nonzero() / user_count)

    artist_rating = (recommendations[:, 1]
                     * (1 - np.array(popularity) * novely_level * 6))
    recommendation_indexes = artist_rating.argsort()[-n_recommendations:][::-1]
    return list(artist_names[recommendations[recommendation_indexes, 0]
                .astype('int')])


def on_request(ch, method, props, body):
    response = predict(body.decode("utf-8"))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id
                                                     =props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    with open('data/dataset.pkl', 'rb') as f:
        dataset_s = pickle.load(f)

    with open('data/artist_names.pkl', 'rb') as f:
        artist_names = pickle.load(f)

    with open('data/model.pkl', 'rb') as f:
        model = pickle.load(f)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_recommendations')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_recommendations')

    parser = RpcClient()

    print("recommendation service ready")
    channel.start_consuming()