import pika
import psycopg2





def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    symbol = body.decode()
    cur.execute(f"SELECT * FROM company WHERE symbol = '{symbol}'';")
    val = cur.fetchone()
    ch.basic_ack(delivery_tag=method.delivery_tag)



credentials = pika.PlainCredentials('sarna', 'sarna')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
db_conn = psycopg2.connect(database='sarna', user='postgres', host='localhost', password='sarna')
cur = db_conn.cursor()
channel = connection.channel()
channel.queue_declare(queue='predict_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='predict_queue', on_message_callback=callback)
channel.start_consuming()