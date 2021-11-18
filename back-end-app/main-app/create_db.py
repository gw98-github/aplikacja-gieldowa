from datetime import timedelta
import random
from typing import List
from app import db
from models import Apisource, Stock, Company, Action
from misc import dane_z_nikad

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


def drop_table(table_name):
    engine = create_engine(DATABASE_URI)
    base = declarative_base()
    metadata = MetaData(engine)
    print(metadata.tables)
    #base.metadata.drop_all(engine, [table], checkfirst=True)
    

def clear_db(db):
    print('Removing Action, Company, Stock, Apisource tables...')

    drop_table('action')



    print('Creating Action, Company, Stock, Apisource tables...')
    db.create_all()
    db.session.commit()
    drop_table('action')

clear_db(db)