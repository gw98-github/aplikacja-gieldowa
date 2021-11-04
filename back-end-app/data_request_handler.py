from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
import random

def dane_z_nikad():
  td = timedelta(hours=1)
  begin = datetime.now()-timedelta(hours=100)
  data = {}
  value = 400
  for e in range(100):
      value = max(100, value + int((random.random() * 2 - 1)**7 * 100))
      data[begin.strftime('%d-%m-%Y %H:00')] = value
      begin += td
  
  final_ret = {"data":data}

  return final_ret

class DataRequestHandler(Resource):

  def get(self):
    return dane_z_nikad()


  def post(self):
    print(self)
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
    ret_status = request_type
    ret_msg = request_json
    td = timedelta(hours='100')
    begin = (datetime.now()-td).strftime('%m-%d-%Y;%H-%M-%S')
    density = 'hour'
    data = [400 for x in range(100)]
    for e, d in enumerate(data[1:]):
        data[e+1] =  max(100, data[e] + int((random.random() * 10)**2))
    
    final_ret = {"data":data}

    return final_ret