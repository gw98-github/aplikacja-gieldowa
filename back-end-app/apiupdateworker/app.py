import pika
import yfinance as yf
import psycopg2
from datetime import datetime, timedelta
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

def request_data(message):
    credentials = pika.PlainCredentials('sarna', 'sarna')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()


try:
    db_conn = psycopg2.connect(database='sarna', user='postgres', host='postgress', password='sarna')
except:
    db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')

def dt_to_timestamp(date):
    return int(datetime.timestamp(date))

def timestamp_to_dt(timestamp):
    return datetime.fromtimestamp(timestamp)


step_seconds=45*60


def run(): 
    print(f"\t  [x] Starting checking...")
    cur = db_conn.cursor()

    find_company = "SELECT * FROM company ;"
    while True:
        start=datetime.now()
        cur.execute(find_company)

        companies = cur.fetchall()
        print(f"\t  [x] Got {len(companies)} companies...")
        updates = 0
        for company_id,c_name,c_symbol,c_stock in companies:
            sql = "SELECT * FROM action WHERE company_id = %s order by timestamp DESC;"
            cur.execute(sql, (company_id,))
            action = cur.fetchone()
            action_dt = timestamp_to_dt(action[2])
            current_company = yf.Ticker(c_symbol)
            values = current_company.history(start=action_dt+timedelta(hours=1), interval='1d')
            time_data = []
            for i in values.index:
                dt = i.to_pydatetime()
                time_data.append((int(1000 * values.at[i,"Open"]), int(datetime.timestamp(dt))))
            if time_data[0][0]==action[1]:
                time_data=time_data[1:]
            sql = "INSERT INTO action(value, timestamp, company_id) VALUES(%s,%s,%s)"
            if len(time_data) > 0:
                updates += 1
            for r in time_data:
                cur.execute(sql, (r[0], r[1], company_id))
                db_conn.commit()
            time.sleep(1)
        end=datetime.now()
        delta=end-start
        print(f"\t  [x] Updated {updates} companies.")
        print(f"\t  [x] Waiting {step_seconds-delta.seconds} seconds...")
        time.sleep(max(0,step_seconds-delta.seconds))
print('[X]   Connected to all.')
run()

