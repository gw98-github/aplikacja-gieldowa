import pika
import yfinance as yf
import psycopg2
from datetime import datetime


# dersja do dockera:
#db_conn = psycopg2.connect(database='sarna', user='postgres', host='postgress', password='sarna')
# wersja z reki:
db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')
cur = db_conn.cursor()

def run():
    #... petla tutaj
    pass
