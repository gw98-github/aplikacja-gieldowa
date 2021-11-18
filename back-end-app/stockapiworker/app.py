import pika
import yfinance as yf


credentials = pika.PlainCredentials('sarna', 'sarna')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


def get_company_data(self,symbol):
    company = yf.Ticker(symbol)
    info = company.info
    name = info["longName"]
    values = company.history(period="2y", interval='1h')
    List = []
    for i in values.index:
        List.append((i.to_pydatetime().strftime('%Y-%m-%dT%H:%M:00'),values.at[i,"Open"]))
    return {'symbol':symbol, 'name':name, 'records':List}



def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    cmd = body.decode()
    
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()