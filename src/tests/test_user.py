import unittest
import json
from flask import url_for
from application import create_app

token_user = None

class UserTestCase(unittest.TestCase):

    aplicattion = create_app('test')
    access_token_twitter = '85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq'
    token_secret_twitter = 'FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf'

    def setUp(self):
        '''
        () -> NoneType
        carga la configuracion necesaria para realizar el test_user,
        se crea un test_client desde el cual se podra ejecutar los
        servicios
        '''

        global token_user
        self.app = self.aplicattion
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        if not token_user:
            token_user = self.get_token()

    def get_token(self):
        resultado = self.client.post(url_for('endpoints.auth_user'
                                    , access_token=self.access_token_twitter
                                    , token_secret=self.token_secret_twitter))
        json_data = json.loads(resultado.data.decode('utf-8'))
        return json_data[0]['token_user']

    def test_get_user_key_twitter(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/user/ -> GET)

        verifica:
            * Los datos requeridos sean proporcionados.
            * Los datos solicitados por el servicio tengan el formato adecuado
            * El usuario se encuentre registrado.
            * El response sea el correcto retorna los datos del usuario y
              status_code = 202 (Proceso exitoso)
        '''

        resultado_exitoso = [{"email": None
                         , "hash_key": "85721956"
                         , "key": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea"
                         , "link_image": "http://abs.twimg.com/sticky/" +
                         "default_profile_images/default_profile_5_normal.png"
                         , "name": "anroco"
                         , "nickname": "anroco"
                         , "registered": "2014-05-09 23:59:59"
                         , "score_answers": 827377
                         , "skills": ["python", "flask", "dynamodb"]
                         , "total_post": 2983}]
        resultado_exitoso_basico = [{"email": None
                         , "hash_key": "85721956"
                         , "key": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea"
                         , "link_image": "http://abs.twimg.com/sticky/" +
                         "default_profile_images/default_profile_5_normal.png"
                         , "name": "anroco"
                         , "nickname": "anroco"
                         , "registered": None
                         , "score_answers": 0
                         , "skills": ["python", "flask", "dynamodb"]
                         , "total_post": 0}]

        #El campo hash_key es requerido y no es suministrado, status_code = 400
        resultado = self.client.get(url_for('endpoints.user'))
        self.assertTrue(resultado.status_code == 400)

        #El tipo de dato proporcionado no tiene el formato adecuado,
        #status_code = 400
        resultado = self.client.get(url_for('endpoints.user'
                                            , hash_key='85721956', basic='si'))
        self.assertTrue(resultado.status_code == 400)

        #El usuario no existe, status_code = 404
        resultado = self.client.get(url_for('endpoints.user', hash_key='0000'))
        self.assertTrue(resultado.status_code == 404)

        #Solicitud con todos los datos correctos y basic=False,
        #proceso satisfactorio, status_code = 200
        resultado = self.client.get(url_for('endpoints.user'
                                            , hash_key='85721956'))
        json_data = json.loads(resultado.data.decode('utf-8'))
        self.assertListEqual(resultado_exitoso, json_data)
        self.assertTrue(resultado.status_code == 200)

        #Solicitud con todos los datos correctos y basic=True
        #proceso satisfactorio, status_code = 200
        resultado = self.client.get(url_for('endpoints.user'
                                            , hash_key='85721956', basic=True))
        json_data = json.loads(resultado.data.decode('utf-8'))
        self.assertListEqual(resultado_exitoso_basico, json_data)
        self.assertTrue(resultado.status_code == 200)

    def test_get_user_nickname(self):
        '''
        () -> NoneType
        realiza pruebas al recurso (/api/1.0/user/<string:nickname> -> GET)

        verifica:
            * El usuario se encuentra registrado.
            * El response sea el correcto retorna los datos del usuario y
              status_code = 200 (Proceso exitoso)
        '''

        resultado_exitoso = [{"hash_key": "85721956"
                        , "key": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea"
                        , "link_image": "http://abs.twimg.com/sticky/" +
                         "default_profile_images/default_profile_5_normal.png"
                        , "skills": ["python", "flask", "dynamodb"]
                        , "token_user": token_user}]

        #El usuario no existe, status_code = 404
        resultado = self.client.get(url_for('endpoints.nickname'
                                            , nickname='no_existe'))
        self.assertTrue(resultado.status_code == 404)

        #Solicitud con todos los datos correctos, proceso satisfactorio
        #status_code = 200
        resultado = self.client.get(url_for('endpoints.nickname'
                                            , nickname='anroco'))
        json_data = json.loads(resultado.data.decode('utf-8'))
        self.assertListEqual(resultado_exitoso, json_data)
        self.assertTrue(resultado.status_code == 200)

    def test_user_scores(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/auth/user/ -> PUT)

        verifica:
            * Los datos requeridos sean proporcionados.
            * Los datos solicitados por el recurso tengan el formato adecuado.
            * El usuario inicio sesion en la aplicacion.
            * El response sea el correcto status_code = 204 (Proceso exitoso)
        '''

        #token_user no validos (usuario no autenticado), status_code = 401
        resultado = self.client.put(url_for('endpoints.user_scores'
                                            , post=True
                                            , answer=False
                                            , token_user='No_Registrado'))
        self.assertTrue(resultado.status_code == 401)

        #Algun campo requerido no es proporcionado, status_code = 400
        resultado = self.client.put(url_for('endpoints.user_scores'))
        self.assertTrue(resultado.status_code == 400)

        #El tipo de dato proporcionado no tiene el formato adecuado,
        #status_code = 400
        resultado = self.client.put(url_for('endpoints.user_scores'
                                            , post='verdadero'
                                            , answer=2
                                            , token_user=token_user))
        self.assertTrue(resultado.status_code == 400)

        #Solicitud con todos los datos correctos, proceso satisfactorio,
        #status_code = 204
        resultado = self.client.put(url_for('endpoints.user_scores'
                                            , post=True
                                            , answer=False
                                            , token_user=token_user))
        self.assertTrue(resultado.status_code == 204)

    def test_register_email(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/auth/register/ -> PUT)

        verifica:
            * Los datos requeridos sean proporcionados.
            * Los datos solicitados por el recurso tengan el formato adecuado.
            * El usuario inicio sesion en la aplicacion.
            * El response sea el correcto status_code = 200 (Proceso exitoso)
        '''

        resultado_exitoso = [{"hash_key": "85721956"
                         , "key": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea"
                         , "link_image": "http://abs.twimg.com/sticky/" +
                         "default_profile_images/default_profile_5_normal.png"
                         , "skills": ["python", "flask", "dynamodb"]
                         , "token_user": token_user}]

        #token_user no validos (usuario no autenticado), status_code = 401
        resultado = self.client.put(url_for('endpoints.user_register'
                                            , email='anroco@dominio.com'
                                            , token_user='No_Registrado'))
        self.assertTrue(resultado.status_code == 401)

        #Algun campo requerido no es proporcionado, status_code = 400
        resultado = self.client.put(url_for('endpoints.user_register'))
        self.assertTrue(resultado.status_code == 400)

        #el campo email no tiene el formato adecuado,
        #status_code = 400
        resultado = self.client.put(url_for('endpoints.user_register'
                                            , email='anroco@dom@inio.com'
                                            , token_user=token_user))
        self.assertTrue(resultado.status_code == 400)

        #Solicitud con todos los datos correctos, proceso satisfactorio,
        #status_code = 200
        resultado = self.client.put(url_for('endpoints.user_register'
                                            , email='anroco@dominio.com'
                                            , token_user=token_user))
        json_data = json.loads(resultado.data.decode('utf-8'))
        self.assertListEqual(resultado_exitoso, json_data)
        self.assertTrue(resultado.status_code == 200)

    def test_users_register_auth(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/login/ -> POST)

        verifica:
            * Los datos requeridos sean proporcionados.
            * Los datos solicitados por el recurso tengan el formato adecuado.
            * El response sea el correcto status_code = 200 (Proceso exitoso)
        '''

        #access_token y/o token_secret no validos (usuario no autorizo la
        #aplicacion para usar el oauth de twitter), status_code = 401
        resultado = self.client.post(url_for('endpoints.auth_user'
                                            , access_token='No_Registrado'
                                            , token_secret='No_Registrado'))
        self.assertTrue(resultado.status_code == 401)

        #Algun campo requerido no es proporcionado, status_code = 400
        resultado = self.client.post(url_for('endpoints.auth_user'))
        self.assertTrue(resultado.status_code == 400)

        #El usuario no ha terminado de registrar su cuenta. Falta registrar
        #el correo electronico, status_code = 428
        resultado = self.client.post(url_for('endpoints.auth_user'
                                    , access_token=self.access_token_twitter
                                    , token_secret=self.token_secret_twitter))
#        self.assertTrue(resultado.status_code == 428)

        #Recuperar el token generado tras la creacion del usuario
        json_data = json.loads(resultado.data.decode('utf-8'))
        token_user = json_data[0]['token_user']

        #registrar el email para realizar un proceso de autenticacion completo.
        resultado = self.client.put(url_for('endpoints.user_register'
                                            , email='anroco@dominio.com'
                                            , token_user=token_user))
        json_data = json.loads(resultado.data.decode('utf-8'))
        self.assertTrue(resultado.status_code == 200)

        #Solicitud con todos los datos correctos, proceso satisfactorio,
        #status_code = 200
        resultado = self.client.post(url_for('endpoints.auth_user'
                                    , access_token=self.access_token_twitter
                                    , token_secret=self.token_secret_twitter))
        #Recuperar el token generado tras la autenticacion del usuario
        json_data = json.loads(resultado.data.decode('utf-8'))
        token_user = json_data[0]['token_user']
        resultado_exitoso = [{"hash_key": "85721956"
                         , "key": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea"
                         , "link_image": "http://abs.twimg.com/sticky/" +
                         "default_profile_images/default_profile_5_normal.png"
                         , "skills": ["python", "flask", "dynamodb"]
                         , "token_user": token_user}]
        self.assertListEqual(resultado_exitoso, json_data)
        self.assertTrue(resultado.status_code == 200)

    def test_get_new_token(self):
        '''
        () -> NoneType
        permite realizar la prueba al recurso (/api/1.0/auth/get_token -> PUT)

        verifica:
            * Los datos requeridos sean proporcionados.
            * El token sea valido.
            * El response sea el correcto status_code = 200 (Proceso exitoso)
        '''
        global token_user

        #Algun campo requerido no es proporcionado, status_code = 400
        resultado = self.client.post(url_for('endpoints.generate_token'))
        self.assertTrue(resultado.status_code == 400)

        #token_user no valido, status_code = 401
        resultado = self.client.put(url_for('endpoints.generate_token'
                                            , token_user='No_Registrado'))
        self.assertTrue(resultado.status_code == 401)

if __name__ == '__main__':
    unittest.main()
