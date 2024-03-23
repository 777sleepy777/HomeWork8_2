import pika
from models import Task
import connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='HW exchange', durable=True)

my_email = "ab1@mnh1.com"
my_fullname = 'Noname_1'

def callback(ch, method, properties, body):
    pk = body.decode()
    task = Task.objects(id=pk, completed=False, email=my_email, consumer_fullname=my_fullname).first()
    if task:
        task.update(set__completed=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue="HW_queue", on_message_callback=callback)
channel.basic_qos(prefetch_count=1)

if __name__ == '__main__':
    channel.start_consuming()