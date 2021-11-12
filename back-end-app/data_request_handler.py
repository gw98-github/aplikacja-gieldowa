from typing import List
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
import random

from sqlalchemy import func, desc
from app import db
from models import Company, Action, Stock, Apisource

from misc import dane_z_nikad

class ActionDataRequestHandler(Resource):

  def get(self, company=None):
    return self.fetch_company_data(company)

  def fetch_company_data(self, company_name):
    data = {'company': company_name}

    company = Company.query.filter(Company.company_name == company_name).all()[0]

    actions = Action.query.filter(Action.company_id==company.id).order_by(desc(Action.timestamp)).limit(100)[::-1]
    actions = [(action.timestamp.strftime('%Y-%m-%dT%H:%M:00'), action.value) for action in actions]

    data['data'] = {t[0]:t[1] for t in actions[:-20]}
    data['predict'] = {t[0]:t[1] for t in actions[-21:]}

    return data

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