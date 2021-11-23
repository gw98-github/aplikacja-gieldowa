from datetime import timedelta
import random
from typing import List
from app import db
from models import Apisource, Stock, Company, Action
from misc import dane_z_nikad
import psycopg2
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base



db_user = 'postgres'
db_password = 'sarna'
db_host = 'localhost'
db_port = 5432
db_name = 'sarna'

DATABASE_URI = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

try:
    from tqdm import tqdm
    TQDM=True
except:
    TQDM=False
    print("Consider instaling tqdm package for your Python interpreter:\npy -m pip install tqdm")

def create_apisource(db, name:str):
    apisource = Apisource(name)
    db.session.add(apisource)
    db.session.commit()
    return apisource.id

def create_stock(db, name:str, apisource_id:int):
    stock = Stock(name, apisource_id)
    db.session.add(stock)
    db.session.commit()
    return stock.id

def drop_table(db_conn, cur, table_name):
    try:
        cur.execute(f"DELETE FROM {table_name}") 
    except:
        pass
    db_conn.commit()
    rows_deleted = cur.rowcount
    return rows_deleted
    

def clear_db(db):
    print('Removing Action, Company, Stock, Apisource tables...')

    db_conn = psycopg2.connect(database='sarna', user='postgres', host='0.0.0.0', password='sarna')
    cur = db_conn.cursor()
    #cur.execute(f"DROP TABLE IF EXISTS action CASCADE") 
    #cur.execute(f"DROP TABLE IF EXISTS company CASCADE") 
    #cur.execute(f"DROP TABLE IF EXISTS stock CASCADE") 
    #cur.execute(f"DROP TABLE IF EXISTS api_source CASCADE") 
    print(f"Deleting actions {drop_table(db_conn, cur, 'action')}")
    print(f"Deleting company {drop_table(db_conn, cur, 'company')}")
    print(f"Deleting stock {drop_table(db_conn, cur, 'stock')}")
    print(f"Deleting apisource {drop_table(db_conn, cur, 'api_source')}")
    


    print('Creating Action, Company, Stock, Apisource tables...')
    db.create_all()
    print('Creating apisource...')
    api_id = create_apisource(db, 'Yahoo')
    print('Creating stock...')
    stock_id = create_stock(db, 'SomeStock', api_id)
    db.session.commit()

clear_db(db)