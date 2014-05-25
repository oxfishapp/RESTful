# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask.ext.restful import Resource, reqparse, marshal_with
from commons import hashValidation, item_to_dict
from formats import format_timeline
from dynamoDBqueries import Skill

cskill = Skill()

class Skill_Table(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('key_user', type=hashValidation, required=False)
        self.reqparse.add_argument('key_post', type=hashValidation, required=False)
        self.reqparse.add_argument('jsonskills', type=str, required=False)
        super(Skill_Table, self).__init__()  
        
    def post(self):
        """
        
        #Se ingresa los datos cuando se realiza una pregunta
        #Se ingresan los datos cuando un usuario se registre
        """
        
        #curl http://localhost:5000/skills -d 'key_post=12EC2020-3AEA-4069-A2DD-08002B30309B' -d 'jsonskills=["csharp","html","jquery"]' 
        #-d 'key_user=fedcf7af-e9f0-69cc-1c68-362d8f5164ea' 
        
        args = self.reqparse.parse_args()
        
        import json
        skillsList = json.loads(args.jsonskills)
        
        keyPost = args.get('key_post')
                
        if not keyPost:
            cskill.put_skills_user(skillsList,args.key_user)
        else:
            cskill.put_skills_post(skillsList,hashValidation(keyPost))
    
        return 'Ingreso'

    @marshal_with(format_timeline)
    def get(self, skill):
        """
        
        
        se consulta cuando se hace un click en skills 
        o por busqueda en url
        """
        
        results = list()
        skills = cskill.finder(skill)

        from dynamoDBqueries import Timeline
        timeline = Timeline()
        
        for skill in skills:
            post = timeline.get_post(skill._data['key_post'])
            post_and_user = item_to_dict(post._data)
            results.append(post_and_user)

        return results             

#Se consulta para saber si una habilidad ya tiene
#personas relacionadas.
class Skill_count(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('skill', type=str, required=True)
        super(Skill_count, self).__init__()  
    
    def get(self):  
#       curl http://localhost:5000/api/1.0/totalskills -d 'skill=dynamodb'  -X GET

        args = self.reqparse.parse_args()

        totalUsers = cskill.count(args.skill)
        
        return {args.skill : totalUsers}
























