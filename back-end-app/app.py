from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
import sqlalchemy
#from flask_cors import CORS #comment this on deployment
from data_request_handler import DataRequestHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='', static_folder='frontend/build')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:sarna@localhost:5432/sarna'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
migrate = Migrate(app, db)



#CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(DataRequestHandler, '/flask/data')

class Apisource(db.Model):
    __tablename__ = 'api_source'
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(80), unique=True, nullable=False)
    last_checked = db.Column(db.DateTime, nullable=False)


class Stock (db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(80), unique=False, nullable=False)
    last_checked = db.Column(db.DateTime, nullable=False)
    api_id = db.Column(db.Integer, db.ForeignKey('api_source.id'))


class Company (db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(80), unique=False, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))


class Action (db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))



if __name__ == '__main__':
    app.run()
