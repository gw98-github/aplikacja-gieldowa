from flask import Flask, send_from_directory, request, redirect, render_template
from flask_restful import Api, Resource, reqparse
import sqlalchemy
#from flask_cors import CORS #comment this on deployment

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import config
import time

import pika

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

from models import UserRequest, UserDataPoint
@app.route("/flask/upload_data", methods=["GET", "POST"])
def upload_datafile():

    if request.method == "POST":
        if not ('modelId' in request.values and 'dataFile' in request.files):
            return {'message':'Invalid data! Provide model id in value "modelId" and the file in "dataFile".'}
        file = request.files['dataFile']
        lines = file.read().decode().split('\n')
        if ';' in lines[0]:
            separator = ';'
        else:
            separator = ','
        if len(lines) == 1:
            try:
                data = [float(x) for x in lines.split(separator)]
            except:
                return {'msg':'parsing error'}
        else:
            data = [l.split(separator)[-1] for l in lines]
            try:
                x = float(data[0])
            except:
                data = data[1:]
            try:
                data = [float(d) for d in data]
            except:
                return {'msg':'parsing error'}
            
        request_id = int(time.time() * 1000)
        ur = UserRequest(request_id, 0, 0)
        db.session.add(ur)
        db.session.commit()
        
        for e, d in enumerate(data):
            db.session.add(UserDataPoint(ur.id, int(d * 1000), e))
        db.session.commit()

        credentials = pika.PlainCredentials('sarna', 'sarna')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='pred_queue_0', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='pred_queue_0',
            body=f'ur;{request_id}',
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()

    return {'request_id':f'{request_id}'}

from data_request_handler import ActionDataRequestHandler, AddCompanyRequestHandler, CandidateRequestHandler, CompanyDataRequestHandler, CurrentModelRequestHandler, PopularCompanyRequestHandler, PredictRequestHandler, OwnPredictionRequestHandler


api.add_resource(ActionDataRequestHandler, '/flask/data/<company>')
api.add_resource(AddCompanyRequestHandler, '/flask/add_company/<symbol>')
api.add_resource(PredictRequestHandler, '/flask/predict/<symbol>')
api.add_resource(CompanyDataRequestHandler, '/flask/list/companies')
api.add_resource(PopularCompanyRequestHandler, '/flask/popular')
api.add_resource(CandidateRequestHandler, '/flask/candidates')
api.add_resource(CurrentModelRequestHandler, '/flask/predictors')
api.add_resource(OwnPredictionRequestHandler, '/flask/own_prediction/<request_id>')

if __name__ == '__main__':

    db.create_all()
    app.run()
