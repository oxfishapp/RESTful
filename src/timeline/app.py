'''
Created on May 8, 2014

@author: Emerson
'''
#!/usr/bin/env python
#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext import restful
from boto.dynamodb2.layer1 import DynamoDBConnection #DynamoDB Conexion
from boto.dynamodb2.table import Table
from flask.ext.restful import Resource, reqparse, fields, marshal_with, marshal
from boto.dynamodb2.items import Item

app = Flask(__name__)
api = restful.Api(app)

#Conexion
conn = DynamoDBConnection(
    host                    =   'localhost'
   ,port                    =   8000
   ,aws_access_key_id       =   'DEVDB' #anything will do
   ,aws_secret_access_key   =   'DEVDB' #anything will do
   ,is_secure               =   False
                        )

table_Timeline = Table('TimelineV11', connection=conn)


class Set_to_List(fields.Raw):
    def format(self, value):
        return list(value)

format_timeline= {
          'Keys':
              {
              'HashKey': fields.String(attribute='Key_Post')
              ,'HashKeyOriginal': fields.String(attribute='Key_PostOriginal')
              }
           ,'Geolocation': fields.String
           ,'FlagAnswer': fields.Integer
           ,'Tags': Set_to_List
           ,'Key_TimelinePost':fields.String
           ,'Key_User':fields.String
           ,'Message140':fields.String
           ,'TotalAnswers':fields.Integer
           ,'WinAnswers':Set_to_List
           ,'Link':fields.String
           ,'Source':fields.String
          }

def WinAnswers(value):
    import json
    list_WinAnswers = []
    for item in json.loads(value):
        list_WinAnswers.append({'Key_Post': item})
    return list_WinAnswers

parser = reqparse.RequestParser()
parser.add_argument('WinAnswers', type=WinAnswers)
parser.add_argument('FlagAnswer', type=int)

class GAI_TimelinePublic(restful.Resource):
    
    @marshal_with(format_timeline)
    def post(self):
        args = parser.parse_args()
        value = args.FlagAnswer
        data = table_Timeline.query_2(
                FlagAnswer__eq=value
                ,limit=20
                ,index='GAI_TimelinePublic'
                #,exclusive_start_key=_exclusive_start_key
                                    )
        result = []
        for item in data:
            result.append(dict(item))
            
        return result

class GAI_VerTodoPublic(restful.Resource):
    
    @marshal_with(format_timeline)
    def get(self, key):
        data = table_Timeline.query_2(
                Key_PostOriginal__eq=key
                ,limit=20
                ,index='GAI_VerTodoPublic'
                #,exclusive_start_key=_exclusive_start_key
                                    )
        result = []
        for item in data:
            result.append(dict(item))
            
        return result
    
    @marshal_with(format_timeline)
    def post(self):
        args = parser.parse_args()
        value = args.WinAnswers
        data = table_Timeline.batch_get(value)   
        
        result = []
        for item in data:
            result.append(dict(item))
                                         
        return result
    
class GAI_Home(restful.Resource):
    
    @marshal_with(format_timeline)
    def get(self, key):
        data = table_Timeline.query_2(
                Key_User__eq=key
                ,limit=20
                ,index='GAI_Home'
                #,exclusive_start_key=_exclusive_start_key
                                    )
        result = []
        for item in data:
            result.append(dict(item))
            
        return result

class Table_Timeline(restful.Resource):
    
    def put(self): 
        pass
    
    def delete(self):
        pass

api.add_resource(GAI_TimelinePublic, '/timeline')
api.add_resource(GAI_VerTodoPublic, '/aloneview/<string:key>')
api.add_resource(GAI_Home, '/home/<string:key>')
api.add_resource(GAI_VerTodoPublic, '/winanswers',endpoint='winanswers')

if __name__ == '__main__':
    app.run(debug=True)
    
#curl http://localhost:5000/winanswers -d 'WinAnswers=["31EC2020-3AEA-4069-A2DD-08002B30309D"]' -X POST
#curl http://localhost:5000/home/AEA-4069-A2DD-08002B30309D
#curl http://localhost:5000/aloneview/11EC2020-3AEA-4069-A2DD-08002B30309D
#curl http://localhost:5000/timeline -d 'FlagAnswer=0' -X POST
#curl http://localhost:5000/timeline -d 'FlagAnswer=1' -X POST

