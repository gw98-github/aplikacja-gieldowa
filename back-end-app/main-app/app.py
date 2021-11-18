from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
import sqlalchemy
#from flask_cors import CORS #comment this on deployment

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import config
app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

#CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

from data_request_handler import ActionDataRequestHandler, CompanyDataRequestHandler
api.add_resource(ActionDataRequestHandler, '/flask/data/<company>')
api.add_resource(CompanyDataRequestHandler, '/flask/list/companies')


if __name__ == '__main__':
    db.create_all()
    app.run()
