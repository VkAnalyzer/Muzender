import uuid
import pika
import pickle


class RpcClient:

    def __init__(self, routing_key, host='queue'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.routing_key = routing_key
        self.response = None
        self.corr_id = None

        result = self.channel.queue_declare(exclusive=True, auto_delete=True, arguments={'x-expires': 10**4})
        self.callback_queue = result.method.queue
        self.consumer_tag = self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

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
                                       priority=2,
                                   ),
                                   body=pickle.dumps(body))
        while self.response is None:
            self.connection.process_data_events()
        self.channel.basic_cancel(self.consumer_tag)
        self.channel.queue_delete(queue=self.callback_queue)
        self.connection.close()
        return self.response
