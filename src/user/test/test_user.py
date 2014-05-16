import unittest
import json
from flask import url_for
from user.app.app import create_app


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
        

    def test_get_user_all(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/user/ -> GET) 
          
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
          
        resultado = self.client.get(url_for('endpoint.user', id_t='1'))
          
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'hash_key': '1'
                                ,'id': '550e8400-e29b-41d4-a716-440000000001'
                                ,'nickname': 'nickname_user_1'
                                ,'name' : 'name_user_1'
                                ,'registered': '2013-10-01 23:18:01'
                                ,'link_image': 'http://twitter.com/user_1/image'
                                ,'total_post': 10
                                ,'score_answers': 5
                                }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
          
        resultado = self.client.get(url_for('endpoint.user', id_t='1', basic=True))
          
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'hash_key': '1'
                                ,'id': '550e8400-e29b-41d4-a716-440000000001'
                                ,'nickname': 'nickname_user_1'
                                ,'name' : 'name_user_1'
                                ,'registered': None
                                ,'link_image': 'http://twitter.com/user_1/image'
                                ,'total_post': 0
                                ,'score_answers': 0
                                }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)


    def test_get_user_post(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/post/user/ -> GET) 
            
        verifica que los datos solicitados por el servicio tengan 
        el formato adecuado y valida que el response sea el correcto.
        status_code = 200 
        '''
           
        id_u = '550e8400-e29b-41d4-a716-440000000001'
        resultado = self.client.get(url_for('endpoint.user_post', id_u = id_u))
            
        json_data = json.loads(resultado.data.decode('utf-8'))
        resultado_esperado = [{'hash_key': '1'
                                ,'id': '550e8400-e29b-41d4-a716-440000000001'
                                ,'nickname': 'nickname_user_1'
                                ,'name' : 'name_user_1'
                                ,'registered': None
                                ,'link_image': 'http://twitter.com/user_1/image'
                                ,'total_post': 0
                                ,'score_answers': 0
                                }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
    
    
    def test_create_user(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/user/ -> POST) 
               
        verifica que los datos ingresados tengan el formato adecuado 
        y valida que el response sea el correcto. status_code = 200. 
        Los datos enviados tienen el siguiente formato json:
        {
            'hash_key': value,
            'nickname': value,
            'name' : value,
            'link_image': value,
        }  
        '''
              
        datos = {'hash_key': '10'
                ,'nickname': 'matox'
                ,'name' : 'Maria Tovar'
                ,'link_image': 'http://twitter.com/motax/image'
                }
                  
        resultado = self.client.post(url_for('endpoint.user'
                                             , data=json.dumps(datos, ensure_ascii=False)))
        self.assertTrue(resultado.status_code == 200)
        
        
    def test_update_user(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/user/ -> PUT) 
               
        verifica que los datos ingresados tengan el formato adecuado 
        y valida que el response sea el correcto. status_code = 200. 
        Los datos enviados tienen el siguiente formato json:
        {
            'hash_key': value,
            'nickname': value,
            'name' : value,
            'link_image': value,
        }  
        '''
              
        datos = {'hash_key': '2'
                ,'id': '550e8400-e29b-41d4-a716-440000000002'
                ,'nickname': 'anroco'
                ,'name' : 'Andres Rodriguez'
                ,'registered': '2013-12-01 00:00:01'
                ,'link_image': 'http://twitter.com/anroco/image'
                ,'total_post': 11
                ,'score_answers': 142
                }
                  
        resultado = self.client.put(url_for('endpoint.user'
                                             , data=json.dumps(datos, ensure_ascii=False)))
        json_data = json.loads(resultado.data.decode('utf-8'))        
        resultado_esperado = [{'hash_key': '2'
                ,'id': '550e8400-e29b-41d4-a716-440000000002'
                ,'nickname': 'anroco'
                ,'name' : 'Andres Rodriguez'
                ,'registered': '2013-10-02 23:18:01'
                ,'link_image': 'http://twitter.com/anroco/image'
                ,'total_post': 11
                ,'score_answers': 142
                }]
        self.assertListEqual(resultado_esperado, json_data)
        self.assertTrue(resultado.status_code == 200)
        
if __name__ == '__main__':
    unittest.main()