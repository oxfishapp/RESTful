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
        """() -> list
        
        Recibe tres posibles atributos por parser key_user, key_post
        y un jsonskills para crear uno o varios registros nuevos en 
        la tabla skills, los datos se ingresan asiciados a un Usuario 
        o a un Post.
        
        Formato con el cual se ingresan los atributos
        en la tabla skill:
        
        jsontimeline=
            '["csharp","html","jquery"]'   
         
        key_user= 
            "str" -> UUID  
            
        key_post=
            "str" -> UUID
            
        Examples:
            curl http://localhost:5000/api/1.0/skills 
                -d 'jsonskills=["csharp","html","jquery"]'  
                -d 'key_user=fedcf7af-e9f0-69cc-1c68-362d8f5164ea' 
                
            curl http://localhost:5000/api/1.0/skills 
                -d 'jsonskills=["csharp2","html2","jquery2"]'  
                -d 'key_user=fedcf7af-e9f0-69cc-1c68-362d8f5164ea' 
               
            curl http://localhost:5000/api/1.0/skills 
                -d 'key_post=12EC2020-3AEA-4069-A2DD-08002B30309B' 
                -d 'jsonskills=["csharp","html","jquery"]'  
                
        """
        
        args = self.reqparse.parse_args()
        
        import json
        skillsList = json.loads(args.jsonskills)
        skillsUser =[]
        keyPost = args.get('key_post')
        keyUser = args.get('key_user')
        
        if keyUser:
            skills_user = cskill.skills_from_user(keyUser)
            skillsUser = [skill for skill in skills_user]
            if skillsUser:
                for item in skillsUser:
                    cskill.delete_skill(item._data['skill'], item._data['key_time']) 
            cskill.post_skills_user(skillsList, keyUser)
                
        if keyPost:
            cskill.post_skills_post(skillsList, keyPost)
    
        return 'Ingreso'

    @marshal_with(format_timeline)
    def get(self, skill):
        """(str) -> list
        
        Recibe un string el cual es un skill en la tabla de skill
        con el fin de consultar la linea de tiempo de dicha habilidad.
        
        Example:
        
            curl http://localhost:5000/api/1.0/findbyskill/flask
            
        Result:
        
            [
                {
                    "flag_answer": "True", 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-13 17:24:31", 
                    "key_user": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "11EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": null
                    }, 
                    "link": "Imagen de Pregunta", 
                    "link_image": "http://twitter.com/anroco/image", 
                    "message140": "Howto Create a table with Python in dynamodb from Flask?", 
                    "name": "Andres Rodriguez", 
                    "nickname": "anroco", 
                    "skills": [
                        "flask", 
                        "python", 
                        "dynamodb"
                    ], 
                    "source": "Web", 
                    "total_answers": 3, 
                    "win_answers": [
                        "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "21EC2020-3AEA-4069-A2DD-08002B30309D"
                    ]
                },
                .
                .
                .
    
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


class Skill_count(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fskill', type=str, required=True)
        super(Skill_count, self).__init__()  
    
    def get(self):  
        """() -> dict
        
        Retirna un diccionario en el cual se puede apreciar
        el numero total de personas que poseen una habilidad skill 
        en particular con el objeto de advertir al usuario cuantas personas
        hay disponibles para responder una pregunta.
        
        Example:
            curl http://localhost:5000/api/1.0/totalskills 
            -d 'skill=dynamodb'  
            -X GET
            
        Result:
            {
                "dynamodb": 3
            }

        """

        args = self.reqparse.parse_args()
        skill = args.get('fskill')

        totalUsers = cskill.count(skill)
        return { skill : totalUsers }
























