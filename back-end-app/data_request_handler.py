from typing import List
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
import random

import sqlalchemy
from app import db
from models import Company, Action, Stock, Apisource

from misc import dane_z_nikad

class ActionDataRequestHandler(Resource):

  def get(self, company=None):
    data = {}
    data['data'], historical_final = dane_z_nikad(steps=80, return_final=True)
    data['predict'] = dane_z_nikad(beg_val=historical_final, steps=20)
    data['company'] = str(company)
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
  

class CompanyDataRequestHandler(Resource):

  def get(self):
    data = {}
    data['companies'] = self.fetch_companies_data()
    return data

  def fetch_companies_data(self):
    companies = Company.query.all()
    data = []
    for company in companies:
      company:Company
      data.append({'name':company.company_name, 'record_count':Action.query.filter(Action.company_id==company.id).count()})
    return data
        

  def post(self):
    return {'ERROR':'NOT IMPLEMENTED!'}