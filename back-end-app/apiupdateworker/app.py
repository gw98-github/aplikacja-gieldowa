import pika
from sqlalchemy import sql
import yfinance as yf
import psycopg2
from datetime import datetime
import time



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

cur = db_conn.cursor()

find_company = "SELECT * FROM company ;"
cur.execute(find_company)

company = cur.fetchall()


for company_id,c_name,c_symbol,c_stock in company:
    sql = "SELECT * FROM action WHERE company_id = %s order by timestamp DESC;"
    cur.execute(sql, (company_id,))
    action = cur.fetchall()
    print (action [0])
    current_company = yf.Ticker(c_symbol)
    values = current_company.history(period="1d", interval='1d')
    print (values.index[0].to_pydatetime().strftime('%Y-%m-%dT%H:%M:00'))
    
    #List = []
    #for i in values.index:
        #List.append((i.to_pydatetime().strftime('%Y-%m-%dT%H:%M:00'),values.at[i,"Open"]))


"""def run():

    timeout = time.time() + 60*45

    while True:

        timeless = 0
        if timeless == 45 or timeless > 45 or time.time() > timeout:
    
pass
"""
