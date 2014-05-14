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

table_Timeline = Table('TimelineV14', connection=conn)


class Set_to_List(fields.Raw):
    def format(self, value):
        return list(value)
    
class HashKey_Validation(fields.Raw):
    def format(self, value): 
        return hashValidation(value)

def hashValidation(value):
    import re
    regex = re.compile('[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z', re.I)
    boolhash = regex.match(value)
    if bool(boolhash):
        return value
    #Genera error
    raise NameError('Hash Validation Crash')

def hashCreate(num_bytes):
    import uuid, M2Crypto
    value = uuid.UUID(bytes = M2Crypto.m2.rand_bytes(num_bytes))
    return str(value)

def hashKeyList(value):
    import json
    list_hashkey = []
    values = json.loads(value)
    for item in values:
        list_hashkey.append({'Key_Post': hashValidation(item)})
    return list_hashkey

def timeUTCCreate():
    from datetime import datetime
    datetime.utcnow()
    return str(datetime.utcnow())

format_timeline= {
          'Keys':
              {
              'HashKey': HashKey_Validation(attribute='Key_Post')
              ,'HashKeyOriginal': HashKey_Validation(attribute='Key_PostOriginal')
              }
           ,'Geolocation': fields.String
           ,'FlagAnswer': fields.Integer
           ,'Tags': Set_to_List
           ,'Key_TimelinePost':fields.String
           ,'Key_User':HashKey_Validation
           ,'Message140':fields.String
           ,'TotalAnswers':fields.Integer
           ,'WinAnswers':Set_to_List
           ,'Link':fields.String
           ,'Source':fields.String
          }

parser = reqparse.RequestParser()
parser.add_argument('HashKeyList', type=hashKeyList, default=None, required=False)
parser.add_argument('FlagAnswer', type=int)

#Global All Index Timeline Public
class Timeline_Index(restful.Resource):
    
    @marshal_with(format_timeline)
    def get(self):
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

#Batch Get Timeline Table
class WinAnswers_Table(restful.Resource):
    
    @marshal_with(format_timeline)
    def get(self):
        args = parser.parse_args()
        hashkeylist = args.HashKeyList
        
        data = table_Timeline.batch_get(hashkeylist)   
        result = []   
        for item in data:
            result.append(dict(item))
                                          
        return result
    
#Global All Index VerTodoPublic
class AloneView_Index(restful.Resource):
    
    @marshal_with(format_timeline)
    def get(self, hashKey):
        data = table_Timeline.query_2(
                         Key_PostOriginal__eq=hashKey
                        ,limit=20
                        ,index='GAI_VerTodoPublic'
               #,exclusive_start_key=_exclusive_start_key
               )
   
        result = []
        for item in data:
            result.append(dict(item))
                                                  
        return result

#Global All Index Home
class Home_Index(restful.Resource):
    
    @marshal_with(format_timeline)
    def get(self, hashKey):
        data = table_Timeline.query_2(
                Key_User__eq=hashKey
                ,limit=20
                ,index='GAI_Home'
                #,exclusive_start_key=_exclusive_start_key
                                    )
        result = []
        for item in data:
            result.append(dict(item))
            
        return result

class Timeline_Table(restful.Resource):
    
    def put(self): 
        pass
    
    def delete(self):
        pass

api.add_resource(Timeline_Index, '/timeline')
api.add_resource(AloneView_Index, '/aloneview/<string:hashKey>')
api.add_resource(Home_Index, '/home/<string:hashKey>')
api.add_resource(WinAnswers_Table, '/winanswers')
#api.add_resource(GAI_VerTodoPublic, '/post',endpoint='post')

if __name__ == '__main__':
    app.run(debug=True)
    
#curl http://localhost:5000/winanswers -d 'HashKeyList=["31EC2020-3AEA-4069-A2DD-08002B30309D"]' -X GET
#curl http://localhost:5000/home/AEAF8765-4069-4069-A2DD-08002B30309D
#curl http://localhost:5000/aloneview/11EC2020-3AEA-4069-A2DD-08002B30309D  
#curl http://localhost:5000/timeline -d 'FlagAnswer=0' -X GET
#curl http://localhost:5000/timeline -d 'FlagAnswer=1' -X GET

