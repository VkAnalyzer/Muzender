import pika
import random
import time


def predict(user_id):
    random.seed(user_id)
    return random.choice(['Led Zeppelin',
                          'Jefferson Airplane',
                          'Sixto Rodriguez',
                          'Jimi Hendrix',
                          'Chad VanGaalen'])


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


time.sleep(10)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print("recommendation service ready")
channel.start_consuming()
