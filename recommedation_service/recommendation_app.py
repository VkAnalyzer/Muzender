import pika
import uuid
import random
import time
import pickle


def predict(user_id):
    response = recommender.call(user_id)
    user_music = pickle.loads(response)
    return random.choice(user_music)['artist']

def on_request(ch, method, props, body):
    user_id = int(body)

    print("recommendation for user", user_id)
    response = predict(user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id
                                                     =props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


# TODO move to separate file, add queue parameters
class RpcClient(object):
    def __init__(self):
        self.response = None
        self.corr_id = None

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_user_music',
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


time.sleep(20)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
channel = connection.channel()
channel.queue_declare(queue='rpc_recommendations')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_recommendations')

recommender = RpcClient()

print("recommendation service ready")
channel.start_consuming()
