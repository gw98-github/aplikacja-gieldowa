import pika
import yfinance as yf
import psycopg2


def get_company_data(self,symbol):
    company = yf.Ticker(symbol)
    info = company.info
    name = info["longName"]
    values = company.history(period="2y", interval='1h')
    List = []
    for i in values.index:
        List.append((i.to_pydatetime().strftime('%Y-%m-%dT%H:%M:00'),values.at[i,"Open"]))
    return {'symbol':symbol, 'name':name, 'records':List}

db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')
cur = db_conn.cursor()

def write_in_database(symbol,name,List):
    cur.execute("SELECT id FROM stock")
    stock_id= cur.fetchone()
    company_name=name
    sql = """INSERT INTO company(company_name,symbol,stock_id)
             VALUES(%s) RETURNING id;"""
    cur.execute(sql, (company_name,symbol,stock_id))
    company_id = cur.fetchone()[0]
    db_conn.commit()
    sql = "INSERT INTO actions(value, timestamp, company_id) VALUES(%s)"
    for l in List:
        cur.execute(sql, (l[0],l[1],company_id))
        db_conn.commit()
    return

def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    symbol = body.decode()
    
    
    ch.basic_ack(delivery_tag=method.delivery_tag)



credentials = pika.PlainCredentials('sarna', 'sarna')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')
cur = db_conn.cursor()
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()