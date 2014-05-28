# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from unittest import TestCase
import json
from flask import url_for
from application import create_app
from unittest import main

class SkillsTestCase(TestCase):
    
    aplicattion = create_app('test')
    
    def setUp(self):
        '''
        () -> NoneType
        carga la configuracion necesaria para realizar el test_skills,
        se crea un test_skills desde el cual se podra ejecutar los 
        servicios        
        '''
        
        self.app = self.aplicattion
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
  
    def test_get_findbyskill(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/findbyskill -> GET) 
           
        Test 1.1. Valida que el response sea el correcto.         
                status_code = 200 
        Test 1.2. Verifica que los datos solicitados por el servicio tengan 
                el formato adecuado.         
                status_code = 200 
        Test 2. Generar un error 400 al no suministrar skill.  
                status_code = 400 

        '''
        resultado = self.client.get(url_for('endpoints.findbyskill'
                                            ,skill='flask'))
           
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado =[
                                {
                                    "flag_answer": "True", 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-13 17:24:31", 
                                    "key_user": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "11EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": None
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
                                }
                            ]

        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
        
        #El campo skill es requerido y no es suministrado en el request
        resultado = self.client.get(url_for('endpoints.findbyskill'))
        self.assertTrue(resultado.status_code == 404)
        
        
    def test_get_totalskills(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/totalskills -> GET) 
            
        Test 1. verifica que los datos solicitados por el servicio tengan 
                el formato adecuado y valida que el response sea el correcto.
                status_code = 200 
        Test 2. Generar un error 400 al no suministrar fskill.
                status_code = 400
        '''
         
        resultado = self.client.get(url_for('endpoints.totalskills'
                                            ,fskill='dynamodb'))
            
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado ={ "dynamodb": 3 }
 
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        self.assertDictEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
        
        #El campo fskill es requerido y no es suministrado en el request
        resultado = self.client.get(url_for('endpoints.totalskills'))
        self.assertTrue(resultado.status_code == 400)
    
    
    def test_post_updateskills(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/skills -> GET) 
            
        Test 1. verifica que los datos se hayan ingresado o acutalizado.
            Test 1.1 key_post
            Test 1.2 key_user
                status_code = 200 
        Test 2. Generar un error 400 al no suministrar jsonskills.
                status_code = 400
        Test 3. Generar un error 400 al no suministrar key_user ni Key_post.
                status_code = 400
        
        '''
        #El campo key_user y jsonskills son suministrados
        #status code 200
        resultado = self.client.post(url_for('endpoints.updateskills'
                                            ,key_user='fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                                            ,jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 200)
        
        #El campo key_post y jsonskills son suministrados
        #status code 200
        resultado = self.client.post(url_for('endpoints.updateskills'
                                            ,key_post='12EC2020-3AEA-4069-A2DD-08002B30309B'
                                            ,jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 200)
        
        #El campo key_user o key post son requeridos y no es 
        #suministrado en el request
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills'
                                            ,jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 400)
        
        #El campo (key_user o key post) y jsonskills son requeridos y no es 
        #suministrado en el request
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills'))
        self.assertTrue(resultado.status_code == 400)
        
        #El campo key_user no tiene el formato adecuado
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills'
                                            ,key_user='zedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                                            ,jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 400)
        
        #El campo key_post no tiene el formato adecuado
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills'
                                            ,key_post='z2EC2020-3AEA-4069-A2DD-08002B30309B'
                                            ,jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 400)
        
    
if __name__ == '__main__':
    main()