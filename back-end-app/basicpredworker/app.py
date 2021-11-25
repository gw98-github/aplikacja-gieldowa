import pika
import psycopg2
from datetime import datetime, timedelta
import random

try:
    db_conn = psycopg2.connect(database='sarna', user='postgres', host='postgress', password='sarna')
except:
    db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')
cur = db_conn.cursor()

def run_model(steps:int=100, end:datetime=None, step_time:timedelta=None, beg_val:int=400, 
    stringify=False, fluctuation=100, as_tuples:bool=False):
    if not step_time:
        step_time = timedelta(hours=1)
    if not end:
        end = datetime.now()
    begin = end-step_time*steps
    data = []
    value = beg_val
    for e in range(steps):
        value = max(100, value + (random.random() * 2 - 1)**5 * fluctuation)
        if stringify:
            data.append((begin.strftime('%d-%m-%Y %H:%M:00'), value))
        else:
            data.append((begin, value))
        begin += step_time
    if as_tuples:
        return data
    return {t[0]: t[1] for t in data}


def callback(ch, method, properties, body):
    symbol = body.decode()
    print(f"\t[x] Received request for {symbol}")
    find_company = "SELECT * FROM company WHERE symbol = %s;"
    cur.execute(find_company, (symbol,))
    company = cur.fetchone()
    if not company:
        print(f"\t[x] No such company: {symbol}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    company_id, company_name, symbol, stock_id = company
    print(f"\t[x] Found company: {symbol} ({company_name})")
    get_future = "SELECT * FROM future WHERE company_id = %s"
    cur.execute(get_future, (company_id,))
    future = cur.fetchone()
    now = int(datetime.timestamp(datetime.now()))
    if not future:
        print(f"\t[x] No future found, creating one...")
        add_future = """INSERT INTO future(company_id,timestamp)
             VALUES(%s,%s) RETURNING id;"""
        cur.execute(add_future, (company_id,now))
        future_id = cur.fetchone()[0]
        db_conn.commit()
    else:
        print(f"\t[x] Found future, cleaning...")
        future_id = future[0]
        delete_preds = "DELETE FROM prediction WHERE company_id = %s;"
        cur.execute(delete_preds, (future_id,))
        db_conn.commit()
    print(f"\t[x] Clean future")
    now_dt = datetime.now() + timedelta(days=20)
    steps = 20
    newest_action_sql = "SELECT * FROM action WHERE company_id = %s ORDER BY timestamp DESC;"
    cur.execute(newest_action_sql, (company_id,))
    action_id, action_value, action_timestamp, action_company_id = cur.fetchone()
    print(f"\t[x] Predicting {steps} steps...")

    pred = run_model(steps=steps, end=now_dt, step_time=timedelta(days=1), as_tuples=True, beg_val=action_value / 1000.0)

    sql = "INSERT INTO prediction(value, timestamp, company_id) VALUES(%s,%s,%s)"
    print(f"\t[x] Inserting into future...")
    cur.execute(sql, (action_value, action_timestamp, future_id, ))
    db_conn.commit()
    for r in pred:
        cur.execute(sql, (int(r[1] * 1000), int(datetime.timestamp(r[0])), future_id))
        db_conn.commit()
    print(f"\t[x] Future done!")

    ch.basic_ack(delivery_tag=method.delivery_tag)



credentials = pika.PlainCredentials('sarna', 'sarna')
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
except:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0', credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='basicpred_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='basicpred_queue', on_message_callback=callback)
print('[X]   Connected to all. Starting consuming queue...')
channel.start_consuming()