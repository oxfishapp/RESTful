from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from flask.ext.restful import Resource, reqparse, marshal_with
from formats import timeline
from factory import hashKeyList, resultSet_to_list


conn = DynamoDBConnection(
    host                    =   'localhost'
   ,port                    =   8000
   ,aws_access_key_id       =   'DEVDB' #anything will do
   ,aws_secret_access_key   =   'DEVDB' #anything will do
   ,is_secure               =   False
                        )

table_Timeline = Table('TimelineV14', connection=conn)

#Global All Index Timeline Public
class Timeline_Index(Resource):
    decorators = [marshal_with(timeline)]
    
    def get(self):
        data = table_Timeline.query_2(
                FlagAnswer__eq=1
                ,limit=20
                ,index='GAI_TimelinePublic'
                #,exclusive_start_key=_exclusive_start_key
                                    )
        return resultSet_to_list(data)

#Batch Get Timeline Table
class WinAnswers_Table(Resource):
    decorators = [marshal_with(timeline)]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('HashKeyList', type=hashKeyList, default=None, required=False)
        super(WinAnswers_Table, self).__init__()
    
    def get(self):
        args = self.reqparse.parse_args()
        hashkeylist = args.HashKeyList
        
        data = table_Timeline.batch_get(hashkeylist)   
        
        return resultSet_to_list(data)
    
#Global All Index VerTodoPublic
class AloneView_Index(Resource):
    decorators = [marshal_with(timeline)]    

    def get(self, hashKey):
        data = table_Timeline.query_2(
                         Key_PostOriginal__eq=hashKey
                        ,limit=20
                        ,index='GAI_VerTodoPublic'
               #,exclusive_start_key=_exclusive_start_key
               )
   
        return resultSet_to_list(data)

#Global All Index Home
class Home_Index(Resource):
    decorators = [marshal_with(timeline)]
    
    def get(self, hashKey):
        data = table_Timeline.query_2(
                Key_User__eq=hashKey
                ,limit=20
                ,index='GAI_Home'
                #,exclusive_start_key=_exclusive_start_key
                                    )
        return resultSet_to_list(data)

class Timeline_Table(Resource):
    
    def put(self): 
        pass
    
    def delete(self):
        pass