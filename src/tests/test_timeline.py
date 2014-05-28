import unittest
import json
from flask import url_for
from application import create_app


class TimelineTestCase(unittest.TestCase):

    aplicattion = create_app('test')

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

    def test_get_public_timeline(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/publictimeline -> GET)

        verifica que los datos solicitados por el servicio tengan
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200
        '''
        resultado = self.client.get(url_for('endpoints.timeline_index'))

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

        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)

    def test_get_home(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/home -> GET) 

        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.timeline_home_index'
                                , key='87654321-e9f0-69cc-1c68-362d8f5164ea'))

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

        
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
    
    def test_get_QandWinA(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/post_qwa -> GET) 
           
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.timeline_qandwina'
                                , key='11EC2020-3AEA-4069-A2DD-08002B30309D'))
           
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


        
        self.assertDictEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
    
    def test_get_answers(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/allanswers -> GET) 
           
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.timeline_answers'
                            , hash_key='11EC2020-3AEA-4069-A2DD-08002B30309D'))
           
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

        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
        
if __name__ == '__main__':
    unittest.main()