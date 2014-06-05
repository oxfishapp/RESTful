# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from unittest import TestCase
import json
from flask import url_for
from devApp import create_app
from unittest import main

token_auth = None
token_anonymous = None


class SkillsTestCase(TestCase):

    aplicattion = create_app('test')
    access_token_twitter = '85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq'
    token_secret_twitter = 'FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf'

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
        self.get_token_anonymous(self.app.config['SECRET_KEY_ANONYMOUS'])
        self.get_token_auth()
 
    def get_token_auth(self):
        '''
        () -> None
 
        Asigna un token para emular un usuario registrado y autenticado.
        '''
 
        global token_auth
        if not token_auth:
            resultado = self.client.post(url_for('endpoints.auth_user',
                                    token_user=token_anonymous,
                                    access_token=self.access_token_twitter,
                                    token_secret=self.token_secret_twitter))
            json_data = json.loads(resultado.data.decode('utf-8'))
            token_auth = json_data['token_user']
        resultado = self.client.put(url_for('endpoints.user_register'
                                            , email='anroco@dominio.com'
                                            , token_user=token_auth))
        self.assertTrue(resultado.status_code == 200)

    def get_token_anonymous(self, secret_key_anonymous):
        '''
        (str) -> None

        Asigna un token para emular un usuario anonimo.
        '''

        global token_anonymous
        from commons import generate_token
        if not token_anonymous:
            token_anonymous = generate_token(secret_key_anonymous)
        
  
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
        resultado = self.client.get(url_for('endpoints.findbyskill',
                                            token_user=token_anonymous,
                                            skill='flask'))
           
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
                                    "link_image": "http://abs.twimg.com/sticky/default_profile_images/default_profile_5_normal.png", 
                                    "message140": "Howto Create a table with Python in dynamodb from Flask?", 
                                    "name": "anroco", 
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

# #         #El campo skill es requerido y no es suministrado en el request
# #         resultado = self.client.get(url_for('endpoints.findbyskill',
# #                                             token_user=token_anonymous))
# #         self.assertTrue(resultado.status_code == 404)
        
        
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
         
        resultado = self.client.get(url_for('endpoints.totalskills',
                                            token_user=token_anonymous,
                                            fskill='dynamodb'))
            
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado ={ "dynamodb": 3 }
 
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        self.assertDictEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
        
        #El campo fskill es requerido y no es suministrado en el request
        resultado = self.client.get(url_for('endpoints.totalskills',
                                            token_user=token_anonymous))
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
        resultado = self.client.post(url_for('endpoints.updateskills',
                                             token_user=token_auth,
                                            key_user='fedcf7af-e9f0-69cc-1c68-362d8f5164ea',
                                            jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 200)
        
        #El campo key_post y jsonskills son suministrados
        #status code 200
        resultado = self.client.post(url_for('endpoints.updateskills',
                                            token_user=token_auth,
                                            key_post='12EC2020-3AEA-4069-A2DD-08002B30309B',
                                            jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 200)
        
        #El campo key_user o key post son requeridos y no es 
        #suministrado en el request
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills',
                                             token_user=token_auth,
                                             jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 400)
        
        #El campo (key_user o key post) y jsonskills son requeridos y no es 
        #suministrado en el request
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills',
                                             token_user=token_auth))
        self.assertTrue(resultado.status_code == 400)
        
        #El campo key_user no tiene el formato adecuado
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills',
                                             token_user=token_auth,
                                             key_user='zedcf7af-e9f0-69cc-1c68-362d8f5164ea',
                                             jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 400)
        
        #El campo key_post no tiene el formato adecuado
        #status code 400
        resultado = self.client.post(url_for('endpoints.updateskills',
                                             token_user=token_auth,
                                             key_post='z2EC2020-3AEA-4069-A2DD-08002B30309B',
                                             jsonskills='["csharp","html","jquery"]'))
        self.assertTrue(resultado.status_code == 400)
        
    
if __name__ == '__main__':
    main()