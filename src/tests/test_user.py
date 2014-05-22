import unittest
import json
from flask import url_for
from application import create_app


class UserTestCase(unittest.TestCase):
    
    aplicattion = create_app('test')
    
    def setUp(self):
        '''
        () -> NoneType
        carga la configuracion necesaria para realizar el test_user,
        se crea un test_client desde el cual se podra ejecutar los 
        servicios        
        '''
        
        self.app = self.aplicattion
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        

    def test_get_user_key_twitter(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/user/ -> GET) 
           
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
           
        resultado = self.client.get(url_for('endpoints.user', hash_key='85721956'))
           
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'hash_key': '85721956'
                               ,'key': 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                               ,'nickname': 'anroco'
                               ,'name' : 'Andres Rodriguez'
                               ,'registered': '2014-05-09 23:59:59'
                               ,'link_image': 'http://twitter.com/anroco/image'
                               ,'total_post': 2983
                               ,'score_answers': 827377
                               ,'email': None
                               }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
           
        resultado = self.client.get(url_for('endpoints.user', hash_key='85721956', basic=True))
           
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'hash_key': '85721956'
                               ,'key': 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                               ,'nickname': 'anroco'
                               ,'name' : 'Andres Rodriguez'
                               ,'registered': None
                               ,'link_image': 'http://twitter.com/anroco/image'
                               ,'total_post': 0
                               ,'score_answers': 0
                               ,'email': None
                               }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
 
 
    def test_get_user_nickname(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/user/<string:nickname> -> GET) 
            
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
            
        resultado = self.client.get(url_for('endpoints.nickname', nickname='anroco'))
            
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'key': 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'}]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
            
  
    def test_get_user_post(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/post/user/ -> GET) 
              
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
             
        key = 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
        resultado = self.client.get(url_for('endpoints.user_post', key = key))
              
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'hash_key': '85721956'
                               ,'key': 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                               ,'nickname': 'anroco'
                               ,'name' : 'Andres Rodriguez'
                               ,'registered': None
                               ,'link_image': 'http://twitter.com/anroco/image'
                               ,'total_post': 0
                               ,'score_answers': 0
                               ,'email': None
                               }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)

        
if __name__ == '__main__':
    unittest.main()