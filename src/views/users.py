'''
Created on May 8, 2014

@author: anroco
'''

from application import dynamodb
from flask import abort, g
from boto.dynamodb2.items import Item
from views.formats import format_user, format_user_twitter, format_user_header
from flask.ext.restful import Resource, marshal_with, reqparse, marshal
from commons import (get_item, validate_email, hashCreate, user_skills,
                     twitter_credentials, timeUTCCreate, generate_token)


db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_user']


class User(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('hash_key', type=str, required=True)

        from flask.ext.restful import types
        self.parser.add_argument('basic', type=types.boolean, default=False)

    @marshal_with(format_user)
    def get(self):
        '''
        () -> list

        requisito: *hash_key* no None

        recibe las solicitudes GET del endpoint ('/api/1.0/user/'). Si el
        atributo *basic* es true, retorna el usuario con los atributos basicos
        definidos en la lista formats.BASIC_USER_FIELDS. Si es false retorna
        el usuario con todos los campos que este tiene. Si el usuario no existe
        se envia un response status_code 404 HTTP.

        curl http://localhost:500/api/1.0/user/
        -d "hash_key=23215634"
        -X GET

        [
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
        ]
        '''

        from .formats import BASIC_USER_FIELDS

        args = self.parser.parse_args()

        #valida el atributo *basic* para definir la consulta a realizar.
        if args.basic:
            result = get_item(table, key_twitter=args.hash_key
                              , attributes=BASIC_USER_FIELDS)
        else:
            result = get_item(table, key_twitter=args.hash_key)
        return [user_skills(result._data)] if result else abort(404)


class Nickname(Resource):

    from api.errors import error_handled

    @marshal_with(format_user_header)
    @error_handled
    def get(self, nickname):
        '''
        (str) -> list

        requisito: nickname no None

        recibe solicitudes GET del endpoint ('/api/1.0/user/<string:nickname>')
        Retorna un json con el key_user del usuario.

        curl http://localhost:5000/api/1.0/user/juanmen

        [
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
        ]
        '''

        result = table.query_2(nickname__eq=nickname
                               , index='nickname_user_index')
        item = result.next()
        return [user_skills(item._data)]


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
        item = g.user_item

        if args.post:
            item._data['total_post'] = int(item._data['total_post']) + 1

        if args.answer:
            item._data['score_answers'] = int(item._data['score_answers']) + 10

        item.save()

        return '', 204


class User_register(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('email', type=validate_email, required=True)

    @marshal_with(format_user_header)
    def put(self):
        '''
        () -> list

        requisito: email debe tener formato

        recibe la solicitud PUT del endpoint ('/api/1.0/auth/register/')
        que permite registrar el correo electronico del usuario.

        Retorna un json con los datos del usuario actualizado.

        curl http://localhost:5000/api/1.0/auth/register/
        -d 'token_user=OiJGbkRtYWFCQnpaYk5GdUJLSkhYbmdaTWYifQ.qiSFiWCltIlgaUHF'
        -d 'email=juanmen@domain.com'
        -X PUT

        [
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
        ]
        '''

        args = self.parser.parse_args()
        item = g.user_item

        item._data['email'] = args.email
        item.save()

        #verificar si se el usuario ya registro sus habilidades
        if not len(g.user_skills):
            abort(428)

        user = item._data
        user['skills'] = g.user_skills
        return [user]


class Auth_user(Resource):

    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('access_token', type=str, required=True)
        self.parser.add_argument('token_secret', type=str, required=True)

    @marshal_with(format_user_header)
    def post(self):
        '''
        () -> list

        requisito: access_token y token_secret no None

        Recibe la solicitud POST del endpoint ('/api/1.0/login/') para
        autenticar un usuario. Se recibe el access_token y token_secret que se
        genero al autenticarse el usuario con su cuenta de twitter. Al final se
        retorna un json con los datos del usuario.

        Se verifica que el access_token y token_secret sean validos. Si el
        usuario no se encuentra registrado se realiza el proceso de registro,
        Si ya se encuentra registrado se realiza una actualizacion de los
        atributos obtenidos desde la cuenta twitter del usuario.

        curl http://localhost:500/api/1.0/login/
        -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq"
        -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf"
        -X POST

        [
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
        ]
        '''

        args = self.parser.parse_args()
        user_tiwtter = twitter_credentials(args.access_token
                                           , args.token_secret)

        #valida la respuesta dada por twitter.
        if user_tiwtter.status != 200:
            abort(401)

        datos = marshal(user_tiwtter.data, format_user_twitter)
        user = get_item(table, key_twitter=datos['key_twitter'])

        token = generate_token(hash_key=user['key_twitter']
                               , access_token=args.access_token
                               , token_secret=args.token_secret)

        #Valida si el usuario ya se encuentra registrado en la base de datos.
        #si no existe se crea y si existe se actualiza.
        if not user:
            datos['registered'] = timeUTCCreate()
            datos['key_user'] = hashCreate()
            datos['token_user'] = token
            user = Item(table, datos)
        else:
            user._data['nickname'] = datos['nickname']
            user._data['name'] = datos['name']
            user._data['link_image'] = datos['link_image']
            user._data['token_user'] = token
        user.save()
        user = user_skills(user._data)

        #verificar si se el usuario ya registro el email y sus habilidades
        if not 'email' in user or user['email'] == '' or \
            not len(user['skills']):
            return [user], 428

        return [user]