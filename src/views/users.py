'''
Created on May 8, 2014

@author: anroco
'''

from dynamoDBqueries import User as UserDB
from flask import abort, g
from views.formats import format_user, format_user_twitter, format_user_header
from flask.ext.restful import Resource, marshal_with, reqparse, marshal
from commons import (validate_email, user_skills, decrypt_token,
                     twitter_credentials)

users = UserDB()


class User(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('hash_key', type=str, required=True)

        from flask.ext.restful import types
        self.parser.add_argument('basic', type=types.boolean, default=False)

    @marshal_with(format_user)
    def get(self):
        '''
        () -> dict

        requisito: *hash_key* no None, *token_user* valido

        recibe las solicitudes GET del endpoint ('/api/1.0/user/'). Si el
        atributo *basic* es true, retorna el usuario con los atributos basicos
        definidos en la lista formats.BASIC_USER_FIELDS. Si es false retorna
        el usuario con todos los campos que este tiene. Si el usuario no existe
        se envia un response status_code 404 HTTP.

        curl http://localhost:500/api/1.0/user/
        -d 'token_user=YbmdaTWYifQqiSFiWCltIlgaUHFOiJGbkRtYW.FCQnpaYk5GdUJLSkh'
        -d "hash_key=23215634"
        -X GET

        {
            "email": juanmen@domain.com,
            "hash_key": "23215634",
            "key": "455597c8-59b6-f6cc-a6ed-078986e819fb",
            "link_image": "http://abs.twimg.com/stick/default_profile.png",
            "name": "Juan Mendoza",
            "nickname": "juanmen",
            "registered": "2014-05-21 02:53:55.791210",
            "score_answers": 40,
            "total_post": 4,
            "skills": [
                "python",
                "flask",
                "dynamodb"
            ]
        }
        '''

        from .formats import BASIC_USER_FIELDS

        args = self.parser.parse_args()

        #valida el atributo *basic* para definir la consulta a realizar.
        if args.basic:
            result = users.get_item(key_twitter=args.hash_key,
                                    attributes=BASIC_USER_FIELDS)
        else:
            result = users.get_item(key_twitter=args.hash_key)
        return user_skills(result._data) if result else abort(404)


class Nickname(Resource):

    from api.errors import error_handled

    @marshal_with(format_user_header)
    @error_handled
    def get(self, nickname):
        '''
        (str) -> dict

        requisito: *nickname* no None y *token_user* valido

        recibe solicitudes GET del endpoint ('/api/1.0/user/<string:nickname>')
        Retorna un json con los datos del usuario.

        curl http://localhost:5000/api/1.0/user/juanmen
        -d 'token_user=YbmdaTWYifQqiSFiWCltIlgaUHFOiJGbkRtYW.FCQnpaYk5GdUJLSkh'
        -X GET

        {
            "hash_key": "23215634",
            "key": "455597c8-59b6-f6cc-a6ed-078986e819fb",
            "link_image": "http://abs.twimg.com/stick/default_profile.png",
            "skills": [
                "python",
                "flask",
                "dynamodb"
            ]
        }
        '''
        item = users.get_by_nickname(nickname)
        return user_skills(item._data)


class User_scores(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        from flask.ext.restful import types
        self.parser.add_argument('post', type=types.boolean, default=False)
        self.parser.add_argument('answer', type=types.boolean, default=False)

    @marshal_with(format_user)
    def put(self):
        '''
        () -> list

        requisito: el usuario debe estar autenticado

        recibe la solicitud PUT del endpoint ('/api/1.0/auth/user/') para
        actualizar los totales de post y answers del usuario .

        No retorna nada, solo un response code 204 HTTP.

        curl http://localhost:5000/api/1.0/auth/user/
        -d 'token_user=OiJGbkRtYWFCQnpaYk5GdUJLSkhYbmdaTWYifQ.qiSFiWCltIlgaUHF'
        -d 'post=false'
        -d 'answer=true'
        -X PUT
        '''

        args = self.parser.parse_args()
        users.update_scores(g.user_item, args.post, args.answer)
        return '', 204


class User_register(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('email', type=validate_email, required=True)

    @marshal_with(format_user_header)
    def put(self):
        '''
        () -> dict

        requisito: email debe tener formato de correo electronico y el usuario
        debe estar registrado en la aplicacion.

        recibe la solicitud PUT del endpoint ('/api/1.0/auth/register/')
        permite registrar el correo electronico del usuario.

        Retorna un json con los datos del usuario actualizado.

        curl http://localhost:5000/api/1.0/auth/register/
        -d 'token_user=OiJGbkRtYWFCQnpaYk5GdUJLSkhYbmdaTWYifQ.qiSFiWCltIlgaUHF'
        -d 'email=juanmen@domain.com'
        -X PUT

        {
            "hash_key": "23215634",
            "key": "455597c8-59b6-f6cc-a6ed-078986e819fb",
            "link_image": "http://abs.twimg.com/stick/default_profile.png",
            "skills": [
                "python",
                "flask",
                "dynamodb"
            ]
        }
        '''

        args = self.parser.parse_args()
        user = users.update_email(g.user_item, args.email)

        #verificar si se el usuario ya registro sus habilidades
        if not len(g.user_skills):
            abort(428)

        user['skills'] = g.user_skills
        return user


class Auth_user(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('access_token', type=str, required=True)
        self.parser.add_argument('token_secret', type=str, required=True)

    @marshal_with(format_user_header)
    def post(self):
        '''
        () -> dict

        requisito: *access_token*, *token_secret* no None y *token_user* valido

        Recibe la solicitud POST del endpoint ('/api/1.0/login/') para
        autenticar un usuario. Se recibe el access_token y token_secret que se
        genero al autenticarse el usuario con su cuenta de twitter. Al final se
        retorna un json con los datos del usuario.

        Se verifica que el access_token y token_secret sean validos. Si el
        usuario no se encuentra registrado se realiza el proceso de registro,
        Si ya se encuentra registrado se realiza una actualizacion de los
        atributos obtenidos desde la cuenta twitter del usuario.

        Se retorna un status_code 200 con los datos del usuario creado o
        autenticado, si el usuario no ha registrado un correo o sus habilidades
        se retorna un status_code 428. Si no se tiene registrados esos dos
        atributos no podra realizar alguna actividad que requira estar
        autenticado.

        curl http://localhost:500/api/1.0/login/
        -d 'token_user=YbmdaTWYifQqiSFiWCltIlgaUHFOiJGbkRtYW.FCQnpaYk5GdUJLSkh'
        -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq"
        -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf"
        -X POST

        {
            "hash_key": "23215634",
            "key": "455597c8-59b6-f6cc-a6ed-078986e819fb",
            "link_image": "http://abs.twimg.com/stick/default_profile.png",
            "skills": [
                "python",
                "flask",
                "dynamodb"
            ]
            "token": "OiJGbkRtYWFCQnpaYk5GdUJLSkhYbmdaTWYifQ.qiSFiWCltIlga"
        }
        '''

        args = self.parser.parse_args()
        user_tiwtter = twitter_credentials(args.access_token,
                                           args.token_secret)

        #valida la respuesta dada por twitter.
        if user_tiwtter.status != 200:
            abort(401)

        datos = marshal(user_tiwtter.data, format_user_twitter)
        user = users.create_or_update_user(datos, args.access_token,
                                           args.token_secret)
        user = user_skills(user)

        #verificar si se el usuario ya registro el email y sus habilidades
        if not 'email' in user or user['email'] == '' or \
            not len(user['skills']):
            return user, 428

        return user


class Generate_token(Resource):

    def put(self):
        '''
        () -> str

        requisito: el usuario debe estar registrado en la base de datos, el
        token actual debe ser vigente y debe ser el igual al que tiene
        registrado en la base de datos.

        recibe la solicitud PUT del endpoint ('/api/1.0/auth/get_token/')
        permite generar un  nuevo token para el usuario.

        Retorna el token nuevo.

        curl http://localhost:500/api/1.0/auth/get_token/
        -d 'token_user=YbmdaTWYifQqiSFiWCltIlgaUHFOiJGbkRtYW.FCQnpaYk5GdUJLSkh'
        -X PUT

        "npaYk5GdUJOiJGbkRtYWFCQOiJtYWFCQaTWYGbkRtYWFCQaTWYifQ.qiSFiWCltIlga"
        '''

        item = g.user_item
        datos_token = decrypt_token(item._data['token_user'])
        user_tiwtter = twitter_credentials(datos_token['access_token'],
                                           datos_token['token_secret'])

        #valida la respuesta dada por twitter.
        if user_tiwtter.status != 200:
            abort(401)

        token = users.update_token(item, datos_token['access_token'],
                                   datos_token['token_secret'])
        return token
