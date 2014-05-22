# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from application import dynamodb
from flask.ext.restful import Resource, reqparse, marshal_with
#from formats import format_question
from commons import hashValidation, timeUTCCreate, item_to_dict, get_item
from formats import format_timeline

db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_skills']
table_user = dynamodb.tables['tbl_user']
table_timeline = dynamodb.tables['tbl_timeline']

#Se ingresa los datos cuando se realiza una pregunta
#Se ingresan los datos cuando un usuario se registre
#se consulta cuando se hace un click en skills o por busqueda
#en url
class Skill_Table(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('key_user', type=hashValidation, required=False)
        self.reqparse.add_argument('key_post', type=hashValidation, required=False)
        self.reqparse.add_argument('jsonskills', type=str, required=False)
        super(Skill_Table, self).__init__()  
        
    def post(self):
        
        #curl http://localhost:5000/skills -d 'key_post=12EC2020-3AEA-4069-A2DD-08002B30309B' -d 'jsonskills=["csharp","html","jquery"]' 
        #-d 'key_user=fedcf7af-e9f0-69cc-1c68-362d8f5164ea' 
        
        import json
        
        args = self.reqparse.parse_args()
        skillsList = json.loads(args.jsonskills)
        keyPost = args.get('key_post')
                
        if not keyPost:
            for skill in skillsList:
                table.put_item(data={'key_user' : args.key_user
                                    ,'skill' : skill
                                    ,'key_time' :  timeUTCCreate()})
        else:
            for skill in skillsList:
                table.put_item(data={'skill' : 'q_'+skill
                                    ,'key_time' :  timeUTCCreate()
                                    ,'key_post' : hashValidation(keyPost)})
    
        return 'Ingreso'

    @marshal_with(format_timeline)
    def get(self, skill):
        
        items = table.query_2(skill__eq='q_'+skill
                              , reverse=True
                              , limit=5
                              , index='GII_Find')
        
        results = []
        
        post_table = dynamodb.tables['tbl_timeline']
        
        for item in items:
            post = get_item(table=post_table, key_post=item._data['key_post'])
            post_user = item_to_dict(post._data)
            results.append(post_user)

        return results              

#Se consulta para saber si una habilidad ya tiene
#personas relacionadas.
class Skill_count(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('skill', type=str, required=True)
        super(Skill_count, self).__init__()  
    
    def get(self):
#         
#       curl http://localhost:5000/api/1.0/auth/totalskills -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq" -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf" -d 'skill=dynamodb' 

        args = self.reqparse.parse_args()
        
        totalUsers = table.query_count(skill__eq=args.skill)
        
        return {args.skill:totalUsers}
























