from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
import sqlalchemy
#from flask_cors import CORS #comment this on deployment
from data_request_handler import DataRequestHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sarna@localhost/sarna'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = sqlalchemy(app)

#CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(DataRequestHandler, '/flask/data')

if __name__ == '__main__':
    app.run()