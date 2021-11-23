from typing import List
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
import random
import pika
from sqlalchemy import func, desc
from app import db
from models import Company, Action, Stock, Apisource

from misc import dane_z_nikad

class PredictRequestHandler(Resource):

  def get(self, symbol=None):
    return self.add_company(symbol)

  def add_company(self, symbol):
    
    results = Company.query.filter(Company.symbol == symbol).all()
    if len(results)> 0:
      company = results[0]
      return {'msg': 'present', 'name': company.company_name}
    credentials = pika.PlainCredentials('sarna', 'sarna')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='predict_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='predict_queue',
        body=symbol,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return {'msg': 'adding'}


class AddCompanyRequestHandler(Resource):

  def get(self, symbol=None):
    return self.add_company(symbol)

  def add_company(self, symbol):
    
    results = Company.query.filter(Company.symbol == symbol).all()
    if len(results)> 0:
      company = results[0]
      return {'msg': 'present', 'name': company.company_name}
    credentials = pika.PlainCredentials('sarna', 'sarna')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=symbol,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return {'msg': 'adding'}


class ActionDataRequestHandler(Resource):

  def get(self, company=None):
    return self.fetch_company_data(company)

  def fetch_company_data(self, company_name):
    
    results = Company.query.filter(Company.company_name == company_name).all()
    if len(results)> 0:
      company = results[0]
    else:
      results = Company.query.filter(Company.symbol == company_name).all()
      if len(results)> 0:
        company = results[0]
      else:
        return {'company': 'NONE', 'data': 'NONE', 'predict': 'NONE'}

    data = {'company': company.company_name}
    actions = Action.query.filter(Action.company_id==company.id).order_by(desc(Action.timestamp)).limit(100)[::-1]
    actions = [(datetime.fromtimestamp(action.timestamp).strftime('%Y.%m.%d %H:%M:00'), round(float(action.value / 1000.0), 2)) for e, action in enumerate(actions)]

    data['data'] = {t[0]:t[1] for t in actions[:-20]}
    data['predict'] = {t[0]:t[1] for t in actions[-21:]}

    return data
  

class CompanyDataRequestHandler(Resource):

  def get(self):
    data = {}
    data['companies'] = self.fetch_companies_data()
    return data

  def fetch_companies_data(self):
    companies = Company.query.all()
    data = []
    td = timedelta(days = 7)
    time_border =  datetime.now() - td
    time_border = int(datetime.timestamp(time_border))
    averages = db.session.query(Action.company_id, func.avg(Action.value)).filter(Action.timestamp>time_border).group_by(Action.company_id).all()
    counts = db.session.query(Action.company_id, func.count(Action.timestamp)).group_by(Action.company_id).all()
    companies = {company.id:company.company_name for company in Company.query.all()}

    for avr_record, count_record in zip(averages, counts):
      company:Company
      company_name = companies[avr_record[0]]
      
      data.append({'name':company_name, 'record_count':count_record[1], 'week_avg':round(float(avr_record[1]/1000), 2)})
    return data
        

  def post(self):
    return {'ERROR':'NOT IMPLEMENTED!'}