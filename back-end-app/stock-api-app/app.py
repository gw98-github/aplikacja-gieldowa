import yfinance as yf 
import psycopg2

def get_connection():
    return psycopg2.connect(host='0.0.0.0', database='sarna', user='postgres', password='sarna')



#...