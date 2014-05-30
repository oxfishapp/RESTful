# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

import unittest
import json
from flask import url_for
from devApp import create_app

token_auth = None
token_anonymous = None


class TimelineTestCase(unittest.TestCase):

    aplicattion = create_app('test')
    access_token_twitter = '85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq'
    token_secret_twitter = 'FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf'

    def setUp(self):
        '''
        () -> NoneType
        carga la configuracion necesaria para realizar el test_timeline,
        se crea un test_timeline desde el cual se podra ejecutar los
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

    def test03_get_public_timeline(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/publictimeline -> GET)
 
        Test 1. verifica que los datos solicitados por el servicio tengan
                el formato adecuado y valida que el response sea el correcto.
                status_code = 200
        '''
        resultado = self.client.get(url_for('endpoints.timeline_index',
                                            token_user=token_anonymous))
 
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
 
 
    def test04_get_home(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/home -> GET) 
  
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.timeline_home_index'
                                , key='87654321-e9f0-69cc-1c68-362d8f5164ea',
                                token_user=token_anonymous,))
  
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado =[
                                {
                                    "flag_answer": None, 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-15 17:24:31", 
                                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                    }, 
                                    "link": "link video", 
                                    "link_image": "http://twitter.com/franper/image", 
                                    "message140": "DOS link del video mas respuesta del usuario", 
                                    "name": "Francisco Perez", 
                                    "nickname": "franper", 
                                    "skills": None, 
                                    "source": "Web", 
                                    "total_answers": 0, 
                                    "win_answers": None
                                }, 
                                {
                                    "flag_answer": None, 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-15 17:24:31", 
                                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "41EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                    }, 
                                    "link": "link video", 
                                    "link_image": "http://twitter.com/franper/image", 
                                    "message140": "TRES link del video mas respuesta del usuario", 
                                    "name": "Francisco Perez", 
                                    "nickname": "franper", 
                                    "skills": None, 
                                    "source": "Web", 
                                    "total_answers": 0, 
                                    "win_answers": None
                                }, 
                                {
                                    "flag_answer": "False", 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-13 17:24:31", 
                                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "12EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": None
                                    }, 
                                    "link": None, 
                                    "link_image": "http://twitter.com/franper/image", 
                                    "message140": "Howto preunta sin resolver?", 
                                    "name": "Francisco Perez", 
                                    "nickname": "franper", 
                                    "skills": [
                                        "jquery", 
                                        "html", 
                                        "csharp"
                                    ], 
                                    "source": "Web", 
                                    "total_answers": 0, 
                                    "win_answers": None
                                }
                            ]
  
          
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
          
        #El campo key no tiene el formato adecuado
        #status code 500
        resultado = self.client.get(url_for('endpoints.timeline_home_index'
                                , key='z7654321-e9f0-69cc-1c68-362d8f5164ea',
                                token_user=token_anonymous,))
        self.assertTrue(resultado.status_code == 400)
 
# #         #El campo key es requerido y no es suministrado en el request
# #         #status code 404
# #         resultado = self.client.get(url_for('endpoints.timeline_home_index',
# #                                             token_user=token_anonymous,))
# #         self.assertTrue(resultado.status_code == 404)
 
 
    def test05_get_QandWinA(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/post_qwa -> GET) 
             
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.timeline_qandwina'
                                , key='11EC2020-3AEA-4069-A2DD-08002B30309D',
                                token_user=token_anonymous))
             
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado ={
                                "question": {
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
                                }, 
                                "winanswers": [
                                    {
                                        "flag_answer": None, 
                                        "geolocation": "4.598056,-74.075833", 
                                        "key_timeline_post": "2014-05-15 17:24:31", 
                                        "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                                        "keys": {
                                            "hash_key": "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                                            "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                        }, 
                                        "link": "link video", 
                                        "link_image": "http://twitter.com/franper/image", 
                                        "message140": "DOS link del video mas respuesta del usuario", 
                                        "name": "Francisco Perez", 
                                        "nickname": "franper", 
                                        "skills": None, 
                                        "source": "Web", 
                                        "total_answers": 0, 
                                        "win_answers": None
                                    }, 
                                    {
                                        "flag_answer": None, 
                                        "geolocation": "4.598056,-74.075833", 
                                        "key_timeline_post": "2014-05-14 17:24:31", 
                                        "key_user": "12345678-e9f0-69cc-1c68-362d8f5164ea", 
                                        "keys": {
                                            "hash_key": "21EC2020-3AEA-4069-A2DD-08002B30309D", 
                                            "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                        }, 
                                        "link": "link video", 
                                        "link_image": "http://twitter.com/viejoemer/image", 
                                        "message140": "UNO link del video mas respuesta del usuario", 
                                        "name": "Emerson Perdomo", 
                                        "nickname": "viejoemer", 
                                        "skills": None, 
                                        "source": "Web", 
                                        "total_answers": 0, 
                                        "win_answers": None
                                    }
                                ]
                            }
  
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        self.assertDictEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
           
        #El campo key no tiene el formato adecuado
        #status code 500
        resultado = self.client.get(url_for('endpoints.timeline_qandwina'
                                            , key='z1EC2020-3AEA-4069-A2DD-08002B30309D',
                                            token_user=token_anonymous))
        self.assertTrue(resultado.status_code == 400)
          
# #         #El campo key es requerido y no es suministrado en el request
# #         #status code 404
# #         resultado = self.client.get(url_for('endpoints.timeline_qandwina',
# #                                             token_user=token_anonymous))
# #         self.assertTrue(resultado.status_code == 404)
 
      
    def test06_get_answers(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/allanswers -> GET) 
             
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.timeline_answers'
                                            ,hash_key='11EC2020-3AEA-4069-A2DD-08002B30309D',
                                            token_user=token_anonymous))
             
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado =[
                                {
                                    "flag_answer": None, 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-15 17:24:31", 
                                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                    }, 
                                    "link": "link video", 
                                    "link_image": "http://twitter.com/franper/image", 
                                    "message140": "DOS link del video mas respuesta del usuario", 
                                    "name": "Francisco Perez", 
                                    "nickname": "franper", 
                                    "skills": None, 
                                    "source": "Web", 
                                    "total_answers": 0, 
                                    "win_answers": None
                                }, 
                                {
                                    "flag_answer": None, 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-15 17:24:31", 
                                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "41EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                    }, 
                                    "link": "link video", 
                                    "link_image": "http://twitter.com/franper/image", 
                                    "message140": "TRES link del video mas respuesta del usuario", 
                                    "name": "Francisco Perez", 
                                    "nickname": "franper", 
                                    "skills": None, 
                                    "source": "Web", 
                                    "total_answers": 0, 
                                    "win_answers": None
                                }, 
                                {
                                    "flag_answer": None, 
                                    "geolocation": "4.598056,-74.075833", 
                                    "key_timeline_post": "2014-05-14 17:24:31", 
                                    "key_user": "12345678-e9f0-69cc-1c68-362d8f5164ea", 
                                    "keys": {
                                        "hash_key": "21EC2020-3AEA-4069-A2DD-08002B30309D", 
                                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                                    }, 
                                    "link": "link video", 
                                    "link_image": "http://twitter.com/viejoemer/image", 
                                    "message140": "UNO link del video mas respuesta del usuario", 
                                    "name": "Emerson Perdomo", 
                                    "nickname": "viejoemer", 
                                    "skills": None, 
                                    "source": "Web", 
                                    "total_answers": 0, 
                                    "win_answers": None
                                }
                            ]
  
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
          
        #El campo key no tiene el formato adecuado
        #status code 400
        resultado = self.client.get(url_for('endpoints.timeline_answers'
                                            ,hash_key='z1EC2020-3AEA-4069-A2DD-08002B30309D',
                                            token_user=token_anonymous))
        self.assertTrue(resultado.status_code == 400)
          
        #El campo hash_key es requerido y no es suministrado en el request
        #status code 405
        resultado = self.client.get(url_for('endpoints.timeline_answers',
                                            token_user=token_anonymous))
        self.assertTrue(resultado.status_code == 400)
         
 
    def test07_post_post_q(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/post_q -> GET) 
            
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
         
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        resultado = self.client.post(url_for('endpoints.post_q',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{
                                                          "message140": "Howto work with json in flask?"
                                                        , "source": "web"
                                                        , "geolocation": "4.598056,-74.075833"
                                                        , "skills": ["flask","json","web"]
                                                        , "link": "http://test1/Pregunta"
                                                        , "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea"
                                                    }'''))
        self.assertTrue(resultado.status_code == 200)
         
        #El campo key_user dentro del formato json no tiene el formato adecuado
        #status code 500
        resultado = self.client.post(url_for('endpoints.post_q',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{
                                                          "message140": "Howto work with json in flask?"
                                                        , "source": "web"
                                                        , "geolocation": "4.598056,-74.075833"
                                                        , "skills": ["flask","json","web"]
                                                        , "link": "http://test1/Pregunta"
                                                        , "key_user": "z7654321-e9f0-69cc-1c68-362d8f5164ea"
                                                    }'''))
        self.assertTrue(resultado.status_code == 400)
          
        #El campo jsontimeline  no tiene el formato adecuado
        #status code 500
        resultado = self.client.post(url_for('endpoints.post_q',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{}'''))
        self.assertTrue(resultado.status_code == 400)
          
# #         #El campo jsontimeline es requerido y no es suministrado
# #         #status code 500
# #         resultado = self.client.post(url_for('endpoints.post_q',
# #                                              token_user=token_auth))
# #         self.assertTrue(resultado.status_code == 500)

        #El campo key_user dentro del formato json no es suministrado
        #status code 500
        resultado = self.client.post(url_for('endpoints.post_q',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{
                                                          "message140": "Howto work with json in flask?"
                                                        , "source": "web"
                                                        , "geolocation": "4.598056,-74.075833"
                                                        , "skills": ["flask","json","web"]
                                                        , "link": "http://test1/Pregunta"
                                                    }'''))
        self.assertTrue(resultado.status_code == 400)


    def test08_post_post_a(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/post_a -> GET) 
            
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
         
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        resultado = self.client.post(url_for('endpoints.post_a',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{
                                                          "message140": "see the video"
                                                        , "source": "web"
                                                        , "geolocation": "4.598056,-74.075833"
                                                        , "link": "http://test2/Respuesta"
                                                        , "key_user": "12345678-e9f0-69cc-1c68-362d8f5164ea"
                                                        , "key_post_original" : "12EC2020-3AEA-4069-A2DD-08002B30309D"
                                                    }'''))
        self.assertTrue(resultado.status_code == 200)
         
        #El campo key_user dentro del formato json no tiene el formato adecuado
        #status code 500
        resultado = self.client.post(url_for('endpoints.post_a',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{
                                                          "message140": "see the video"
                                                        , "source": "web"
                                                        , "geolocation": "4.598056,-74.075833"
                                                        , "link": "http://test2/Respuesta"
                                                        , "key_user": "z2345678-e9f0-69cc-1c68-362d8f5164ea"
                                                        , "key_post_original" : "12EC2020-3AEA-4069-A2DD-08002B30309D"
                                                    }'''))
        self.assertTrue(resultado.status_code == 400)
         
        #El campo key_post_original dentro del formato json no tiene el formato adecuado
        #status code 500
        resultado = self.client.post(url_for('endpoints.post_a',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{
                                                          "message140": "see the video"
                                                        , "source": "web"
                                                        , "geolocation": "4.598056,-74.075833"
                                                        , "link": "http://test2/Respuesta"
                                                        , "key_user": "12345678-e9f0-69cc-1c68-362d8f5164ea"
                                                        , "key_post_original" : "z20edb33-4dc7-43c7-bc8b-8ee3365a609b"
                                                    }'''))
        self.assertTrue(resultado.status_code == 400)
         
        #El campo jsontimeline  no tiene el formato adecuado
        #status code 500
        resultado = self.client.post(url_for('endpoints.post_a',
                                    token_user=token_auth,
                                    jsontimeline=
                                                    '''{}'''))
        self.assertTrue(resultado.status_code == 400)
         
# #         #El campo jsontimeline es requerido y no es suministrado
# #         #status code 500
# #         resultado = self.client.post(url_for('endpoints.post_a'))
# #         self.assertTrue(resultado.status_code == 500)
          
# #         #El campo key_user dentro del formato json no es suministrado
# #         #status code 500
# #         resultado = self.client.post(url_for('endpoints.post_a',
# #                                     token_user=token_auth,
# #                                     jsontimeline=
# #                                                     '''{
# #                                                           "message140": "see the video"
# #                                                         , "source": "web"
# #                                                         , "geolocation": "4.598056,-74.075833"
# #                                                         , "link": "http://test2/Respuesta"
# #                                                         , "key_post_original" : "12EC2020-3AEA-4069-A2DD-08002B30309D"
# #                                                     }'''))
# #         self.assertTrue(resultado.status_code == 500)  

    def test10_delete_delete_q_a(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/delete_q_a -> GET) 
            
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
         
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        resultado = self.client.delete(url_for('endpoints.delete_q_a',
                                    token_user=token_auth,
                                    hash_key='41EC2020-3AEA-4069-A2DD-08002B30309D'))
        self.assertTrue(resultado.status_code == 200)
         
        #El campo hash_key no tiene el formato adecuado
        #status code 500
        resultado = self.client.delete(url_for('endpoints.delete_q_a',
                                    token_user=token_auth,
                                    hash_key='z1EC2020-3AEA-4069-A2DD-08002B30309D'))
        self.assertTrue(resultado.status_code == 400)
         
        #El campo hash_key tiene un UUID que no existe en dynamodb
        #status code 500
        resultado = self.client.delete(url_for('endpoints.delete_q_a',
                                    token_user=token_auth,
                                    hash_key='A1EC2020-3AEA-4069-A2DD-08002B30309D'))
        self.assertTrue(resultado.status_code == 404)
         
# #         #El campo hash_key es requerido y no es suministrado 
# #         #status code 500
# #         resultado = self.client.delete(url_for('endpoints.delete_q_a',
# #                                                token_user=token_auth))
# #         self.assertTrue(resultado.status_code == 500)

    def test09_put_update_q(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/update_q -> GET) 
            
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
         
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        resultado = self.client.put(url_for('endpoints.update_q',
                                    token_user=token_auth,
                                    hash_key='11EC2020-3AEA-4069-A2DD-08002B30309D',
                                    jsontimeline='''{
                                                   "state" : 1
                                                  ,"hash_key_answer" : "41EC2020-3AEA-4069-A2DD-08002B30309D"
                                                  }'''))
        self.assertTrue(resultado.status_code == 200)
         
        #El campo hash_key no tiene el formato correcto
        #status code 400
        resultado = self.client.put(url_for('endpoints.update_q',
                                    token_user=token_auth,
                                    hash_key='z1EC2020-3AEA-4069-A2DD-08002B30309D',
                                    jsontimeline='''{
                                                   "state" : 0
                                                  ,"hash_key_answer" : "z1EC2020-3AEA-4069-A2DD-08002B30309D"
                                                  }'''))
        self.assertTrue(resultado.status_code == 400)
         
        #Intentando remover el mismo dato por segunda vez de winanswer
        #status code 500
        resultado = self.client.put(url_for('endpoints.update_q',
                                    token_user=token_auth,
                                    hash_key='z1EC2020-3AEA-4069-A2DD-08002B30309D',
                                    jsontimeline='''{
                                                   "state" : 0
                                                  ,"hash_key_answer" : "z1EC2020-3AEA-4069-A2DD-08002B30309D"
                                                  }'''))
        self.assertTrue(resultado.status_code == 400)
         
        #============================================================
        #------Ingresar el mismo valor dos veces en win answers------
        #============================================================
         
        #Insertando la respuesta en los winanswers por segunda vez
        #el status code 500.
        resultado = self.client.put(url_for('endpoints.update_q',
                                    token_user=token_auth,
                                    hash_key='11EC2020-3AEA-4069-A2DD-08002B30309D',
                                    jsontimeline='''{
                                                   "state" : 1
                                                  ,"hash_key_answer" : "41EC2020-3AEA-4069-A2DD-08002B30309D"
                                                  }'''))
        self.assertTrue(resultado.status_code == 500)
         
        #============================================================
       
        #Valida el resultado esperado con el resultado obtenido y 
        #el status code.
        resultado = self.client.put(url_for('endpoints.update_q',
                                    token_user=token_auth,
                                    hash_key='11EC2020-3AEA-4069-A2DD-08002B30309D',
                                    jsontimeline='''{
                                                   "state" : 0
                                                  ,"hash_key_answer" : "41EC2020-3AEA-4069-A2DD-08002B30309D"
                                                  }'''))
        self.assertTrue(resultado.status_code == 200)
        
if __name__ == '__main__':
    unittest.main()