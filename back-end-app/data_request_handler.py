from typing import List
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
import random

from sqlalchemy import func
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
    td = timedelta(days = 7)
    time_border = datetime.now() - td

    averages = db.session.query(Action.company_id, func.avg(Action.value)).filter(Action.timestamp>time_border).group_by(Action.company_id).all()
    counts = db.session.query(Action.company_id, func.count(Action.timestamp)).group_by(Action.company_id).all()
    companies = {company.id:company.company_name for company in Company.query.all()}

    for avr_record, count_record in zip(averages, counts):
      company:Company
      company_name = companies[avr_record[0]]
      
      data.append({'name':company_name, 'record_count':count_record[1], 'week_avg':avr_record[1]})
    return data
        

  def post(self):
    return {'ERROR':'NOT IMPLEMENTED!'}