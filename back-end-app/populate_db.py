from typing import List
from app import db
from models import Apisource, Stock, Company, Action
from misc import dane_z_nikad

def clear_db(db):
    db.session.query(Action).delete()
    db.session.query(Company).delete()
    db.session.query(Stock).delete()
    db.session.query(Apisource).delete()
    db.session.commit()

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

def create_company(db, name:str, stock_id:int):
    company = Company(name, stock_id)
    db.session.add(company)
    db.session.commit()
    return company.id

def create_actions(db, company_id, steps=1000, base_value=400, fluctuation=100):
    for timestamp, value in dane_z_nikad(steps=steps, beg_val=base_value, fluctuation=fluctuation, stringify=False).items():
        a = Action(value, timestamp, company_id)
        db.session.add(a)
    db.session.commit()

def populate(db, companies:List[str]=['CDP', 'Tesla', 'Game Stop']):
    print('Clearing db...')
    clear_db(db)
    print('Creating apisource...')
    api_id = create_apisource(db, 'Yahoo')
    print('Creating stock...')
    stock_id = create_stock(db, 'Some Stock', api_id)
    print('Creating companies:')
    for company in companies:
        print(f'\tCreating {company}...')
        company_id = create_company(db, company, stock_id)
        create_actions(db, company_id)
    print('Finished :)')

populate(db)