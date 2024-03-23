import pika
from models import Task
import connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW exchange', exchange_type='direct')
channel.queue_declare(queue='HW_queue', durable=True)
channel.queue_bind(exchange="HW exchange", queue="HW_queue")

def create_tasks(nums: int):

    for i in range(nums):
        task = Task(consumer_fullname=f'Noname_{i}', email=f'ab{i}@mnh{i}.com').save()
        channel.basic_publish(
            exchange='HW exchange',
            routing_key='HW_queue',
            body=str(task.id).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()

if __name__ == "__main__":
    create_tasks(10)
