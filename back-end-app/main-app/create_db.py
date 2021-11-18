from datetime import timedelta
import random
from typing import List
from app import db
from models import Apisource, Stock, Company, Action
from misc import dane_z_nikad
try:
    from tqdm import tqdm
    TQDM=True
except:
    TQDM=False
    print("Consider instaling tqdm package for your Python interpreter:\npy -m pip install tqdm")

def clear_db(db):
    print('Removing Action, Company, Stock, Apisource tables...')
    try:
        db.session.query(Action).delete()
    except:
        pass
    try:
        db.session.query(Company).delete()
    except:
        pass
    try:
        db.session.query(Stock).delete()
    except:
        pass
    try:
        db.session.query(Apisource).delete()
    except:
        pass
    print('Creating Action, Company, Stock, Apisource tables...')
    db.create_all()
    try:
        db.session.commit()
    except:
        pass

clear_db(db)