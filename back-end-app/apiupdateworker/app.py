import pika
import yfinance as yf
import psycopg2
from datetime import datetime




def request_prediction(symbol):
    credentials = pika.PlainCredentials('sarna', 'sarna')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='basicpred_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='basicpred_queue',
        body=symbol,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()


try:
    db_conn = psycopg2.connect(database='sarna', user='postgres', host='postgress', password='sarna')
except:
    db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')

def run():
    
    pass

run()

