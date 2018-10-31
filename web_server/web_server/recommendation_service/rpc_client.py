import uuid
import pika
import pickle

connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
channel = connection.channel()

class RpcClient:

    def __init__(self, connection, channel, routing_key):
        self.connection = connection
        self.channel = channel
        self.routing_key = routing_key
        self.response = None
        self.corr_id = None

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = pickle.loads(body)

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id,
                                         ),
                                   body=pickle.dumps(body))
        while self.response is None:
            self.connection.process_data_events()
        self.channel.queue_delete(queue=self.callback_queue)
        return self.response
