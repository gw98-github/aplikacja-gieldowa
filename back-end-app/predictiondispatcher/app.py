import pika
import psycopg2


def callback(ch, method, properties, body):
    symbol = body.decode()
    print(" [x] Received %s" % symbol)
    



credentials = pika.PlainCredentials('sarna', 'sarna')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
db_conn = psycopg2.connect(database='sarna', user='postgres', host='postgress', password='sarna')
cur = db_conn.cursor()
channel = connection.channel()
channel.queue_declare(queue='predict_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='predict_queue', on_message_callback=callback)
print('[X]   Connected to all. Starting consuming queue...')
channel.start_consuming()