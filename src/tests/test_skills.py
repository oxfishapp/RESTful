import unittest
import json
from flask import url_for
from application import create_app

class SkillsTestCase(unittest.TestCase):
    
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
        
    def test_get_totalskills(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/totalskills -> GET) 
           
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.skill_count',skill='dynamodb'))
           
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado ={
                                "dynamodb": 3
                            }

        
        self.assertDictEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
    
    def test_get_findbyskill(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/findbyskill -> GET) 
           
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
        resultado = self.client.get(url_for('endpoints.skill_table',skill='flask'))
           
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
        
if __name__ == '__main__':
    unittest.main()