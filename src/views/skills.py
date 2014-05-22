# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from application import dynamodb
from flask.ext.restful import Resource, reqparse, marshal_with
from formats import format_skill
from commons import hashValidation, timeUTCCreate

db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_skills']
table_user = dynamodb.tables['tbl_users']
table_timeline = dynamodb.tables['tbl_timeline']

#se consulta para poner las habilidades
#en el navigation bar
class Skill_Navbar_Index(Resource):
    #decorators = [marshal_with(format_timeline)]  
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KeyUser', type=hashValidation, required=True)
        super(Skill_Navbar_Index, self).__init__()  
        
        
    def get(self):
        
        args = self.reqparse.parse_args()
        
        skillUser = table.query_2(Key_User__eq=args.KeyUser
                                ,limit=3
                                ,index='GKOI_Navbar'
                                ,reverse=True)
        
        result = []
        for skill in skillUser:
            result.append(skill._data['Skill'])
        
        return result

#Se ingresa los datos cuando se realiza una pregunta
#Se ingresan los datos cuando un usuario se registre
#se consulta cuando se hace un click en skills
class Skill_Table(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KeyUser', type=hashValidation, required=False)
        self.reqparse.add_argument('KeyPost', type=hashValidation, required=False)
        self.reqparse.add_argument('Skills', type=str,action='append', required=True)
        super(Skill_Table, self).__init__()  
        
        def post(self):
            
            args = self.reqparse.parse_args()
            skillsList = args.Skills
            keyPost = args.get('KeyPost')
            
            
            if not keyPost:
                for skill in skillsList:
                    table.put_item(data={'Key_User' : args.KeyUser
                                        ,'Skill' : skill
                                        ,'Skill_User' : 'True'
                                        ,'Key_Time' :  timeUTCCreate()})
            else:
                for skill in skillsList:
                    table.put_item(data={'Skill' : skill
                                        ,'Key_Time' :  timeUTCCreate()
                                        ,'Key_Post' : hashValidation(keyPost)})
        
        return 'Ingreso'
    
    def get(self):
        
        args = self.reqparse.parse_args()
        skillsList = args.Skills
        
        items = table.query_2(Skill__eq=skillsList[0]
                              , reverse=True
                              , limit=5
                              , attributes=('Key_Time','Key_Post','Key_User'))
        
        results = []
        for item in items:
            skill = item._data.items()
            post = table_timeline.get_item(Key_Post=hashValidation(item._data['Key_Post']))._data.items()
            user = table_user.query_2(key_user__eq = hashValidation(item._data['Key_User']), index = 'key_user_index').next()._data.items()
            
            results.append(dict(skill,post,user))
            
   
        return 0                

#Se consulta para saber si una habilidad ya tiene
#personas relacionadas.
class Skill_Count_Table(Resource):
    pass

























