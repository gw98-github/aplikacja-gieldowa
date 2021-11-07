from typing import List
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
import random

import sqlalchemy
from app import db
from models import Company, Action, Stock, Apisource

from misc import dane_z_nikad

class DataRequestHandler(Resource):

  def get(self, company=None, algorythm=None):
    data = {}
    data['data'] = dane_z_nikad()
    data['company'] = str(company)
    data['algorythm'] = str(algorythm)
    self.fetch_company_data('CDP')
    return data

  def fetch_company_data(self, company_name):
    print(Apisource.query.all())
    print(Stock.query.all()[0].api_id)
    print(Company.query.all()[0].stock_id)
    print(Action.query.all()[0].company_id)
        

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('message', type=str)

    args = parser.parse_args()

    print(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

    request_type = args['type']
    request_json = args['message']
    # ret_status, ret_msg = ReturnData(request_type, request_json)
    # currently just returning the req straight

    return dane_z_nikad()