from app import db
from datetime import datetime
class Apisource(db.Model):
    __tablename__ = 'api_source'
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(80), unique=True, nullable=False)
    last_checked = db.Column(db.DateTime, nullable=False)

    def __init__(self, api_name, last_checked=None) -> None:
        super().__init__()
        self.api_name = api_name
        if last_checked:
            self.last_checked = last_checked
        else:
            self.last_checked = datetime.now()


class Stock (db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(80), unique=False, nullable=False)
    last_checked = db.Column(db.DateTime, nullable=False)
    api_id = db.Column(db.Integer, db.ForeignKey('api_source.id'))
    
    def __init__(self, stock_name, api_id, last_checked=None) -> None:
        super().__init__()
        self.stock_name = stock_name
        if last_checked:
            self.last_checked = last_checked
        else:
            self.last_checked = datetime.now()
        self.api_id = api_id


class Company (db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(80), unique=False, nullable=False)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))

    def __init__(self, company_name, symbol, stock_id) -> None:
        super().__init__()
        self.company_name = company_name
        self.symbol = symbol
        self.stock_id=stock_id

class Future (db.Model):
    __tablename__ = 'future'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, company_id, timestamp, stock_id) -> None:
        super().__init__()
        self.company_id = company_id
        self.timestamp=timestamp

class Prediction (db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('future.id'))
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)

    def __init__(self, company_id, timestamp, value) -> None:
        super().__init__()
        self.company_id = company_id
        self.timestamp=timestamp
        self.value = value


class Action (db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    
    def __init__(self, value, timestamp, company_id) -> None:
        super().__init__()
        self.value = value
        self.timestamp = timestamp
        self.company_id = company_id