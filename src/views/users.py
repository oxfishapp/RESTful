'''
Created on May 8, 2014

@author: anroco
'''

from application import dynamodb
from flask import abort, g
from boto.dynamodb2.items import Item
from views.formats import format_user,format_user_twitter
from flask.ext.restful import Resource, marshal_with, reqparse, marshal
from commons import (hashValidation, get_item, validate_email, hashCreate, 
                     twitter_credentials, timeUTCCreate)


db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_user']


class User(Resource):
    
    decorators = [marshal_with(format_user)]
    parser = reqparse.RequestParser()
    
    def __init__(self):
        self.parser.add_argument('hash_key', type=str, required=True)
    
        from flask.ext.restful import types
        self.parser.add_argument('basic', type=types.boolean, default=False)
    
    
    def get(self):
        '''
        () -> list        
        
        requisito: *key_t* no None
        
        recibe las solicitudes GET del endpoint ('/api/1.0/user/'). Si el atributo 
        *basic* es true, retorna el usuario con los atributos basicos 
        definidos en la lista formats.BASIC_USER_FIELDS. Si es false retorna
        el usuario con todos los campos que este tiene.
        
        curl http://201.245.249.229:8080/api/1.0/user/ -d "hash_key=23215634" -X GET
        
        [
            {
                "hash_key": "23215634", 
                "key": "455597c8-59b6-f6cc-a6ed-078986e819fb", 
                "link_image": "http://abs.twimg.com/sticky/default_profile.png", 
                "name": "Juan Mendoza", 
                "nickname": "juanmen", 
                "registered": "2014-05-21 02:53:55.791210", 
                "score_answers": 40, 
                "total_post": 4
            }
        ]
        '''
        
        from .formats import BASIC_USER_FIELDS
        
        args = self.parser.parse_args()
        
        #valida el atributo *basic* para definir el tipo de consulta a realizar.
        if args.basic:
            result = table.get_item(key_twitter = args.hash_key
                                    , attributes = BASIC_USER_FIELDS)
        else:
            result = table.get_item(key_twitter = args.hash_key)
        return [result._data]
    

class Nickname(Resource):

    def get(self, nickname):
        '''
        (str) -> list        
        
        requisito: nickname no None 
        
        recibe las solicitudes GET del endpoint ('/api/1.0/user/<string:nickname>'). 
        Retorna un json con el key_user del usuario. 
        
        curl http://localhost:5000/api/1.0/user/juanmen
        
        [
            {
                "key": "455597c8-59b6-f6cc-a6ed-078986e819fb"
            }
        ]
        '''
        
        result = table.query_2(nickname__eq = nickname, index = 'nickname_user_index')
        return [{'key':result.next()._data['key_user']}]
    

class User_post(Resource):
    
    parser = reqparse.RequestParser()
    
    def __init__(self):
        self.parser.add_argument('key', type=hashValidation, required=True)
    
    
    @marshal_with(format_user)
    def get(self):
        '''
        () -> list        
        
        requisito: key_u debe tener formato uuii(16)
        
        recibe las solicitudes GET del endpoint ('/api/1.0/post/user/')
        y retorna toda la informacion relacionada a ese usuario.
        
        curl http://201.245.249.229:8080/api/1.0/post/user/ 
        -d "key=455597c8-59b6-f6cc-a6ed-078986e819fb" 
        -X GET
        
            [
                {
                    "hash_key": "23215634", 
                    "key": "455597c8-59b6-f6cc-a6ed-078986e819fb", 
                    "link_image": "http://abs.twimg.com/sticky/default_profile.png", 
                    "name": "Juan Mendoza", 
                    "nickname": "juanmen", 
                    "registered": null, 
                    "score_answers": 0, 
                    "total_post": 0
                }
            ]
        '''
        
        args = self.parser.parse_args()
        result = table.query_2(key_user__eq = args.key, index = 'key_user_index')
        return [result.next()._data]


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
        
        recibe la solicitud PUT del endpoint ('/api/1.0/auth/user/') para actualizar 
        los totales de post y answers del usuario .
        
        Retorna un json con los datos del usuario actualizado.
        
            curl http://201.245.249.229:8080/api/1.0/auth/user/ 
            -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq" 
            -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf" 
            -d "post=false" 
            -d "answer=true" 
            -X PUT
            
            [
                {
                    "hash_key": "23215634", 
                    "key": "455597c8-59b6-f6cc-a6ed-078986e819fb", 
                    "link_image": "http://abs.twimg.com/sticky/default_profile.png", 
                    "name": "Juan Mendoza", 
                    "nickname": "juanmen", 
                    "registered": "2014-05-21 02:53:55.791210", 
                    "score_answers": 40, 
                    "total_post": 4
                }
            ]

        '''
        
        args = self.parser.parse_args()
        item = get_item(table, key_twitter = g.id_twitter)
        
        if item == None:
            abort(401)
            
        if args.post: 
            item._data['total_post'] = int (item._data['total_post']) + 1
            
        if args.answer: 
            item._data['score_answers'] = int (item._data['score_answers']) + 10
            
        item.save()
            
        return [item._data]


class User_register(Resource):
     
    parser = reqparse.RequestParser()
     
    def __init__(self):
        self.parser.add_argument('email', type=validate_email, required=True)
             
     
    @marshal_with(format_user)
    def put(self):
        '''
        () -> list        
         
        requisito: email debe tener formato 
         
        recibe la solicitud PUT del endpoint ('/api/1.0/auth/register/') 
        que permite registrar el correo electronico del usuario.
         
        Retorna un json con los datos del usuario actualizado.
         
            curl http://201.245.249.229:8080/api/1.0/auth/register/ 
            -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq" 
            -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf" 
            -d "email=juanmen@domain.com" 
            -X PUT
             
            [
                {
                    "email": "juanmen@domain.com"
                    "hash_key": "23215634", 
                    "key": "455597c8-59b6-f6cc-a6ed-078986e819fb", 
                    "link_image": "http://abs.twimg.com/sticky/default_profile.png", 
                    "name": "Juan Mendoza", 
                    "nickname": "juanmen", 
                    "registered": "2014-05-21 02:53:55.791210", 
                    "score_answers": 40, 
                    "total_post": 4
                }
            ]
 
        '''
         
        args = self.parser.parse_args()
        item = get_item(table, key_twitter = g.id_twitter)
        
        if item == None:
            abort(401)
        
        item._data['email'] = args.email
        item.save()
        return [item._data]
    

class Auth_user(Resource):
    
    parser = reqparse.RequestParser()
    
    def __init__(self):
        self.parser.add_argument('access_token', type=str, required=True)
        self.parser.add_argument('token_secret', type=str, required=True)   
        
        
    @marshal_with(format_user)
    def post(self):
        '''
        () -> list        
        
        requisito: access_token y token_secret no None
        
        Recibe la solicitud POST del endpoint ('/api/1.0/login/') para autenticar 
        un usuario. Se recibe el access_token y token_secret que se genero al 
        autenticarse el usuario con su cuenta de twitter. Al final se retorna 
        un json con los datos del usuario.
        
        Se verifica que el access_token y token_secret sean validos. Si el 
        usuario no se encuentra registrado se realiza el proceso de registro, 
        Si ya se encuentra registrado se realiza una actualizacion de los 
        atributos obtenidos desde la cuenta twitter del usuario.   
        
            curl http://201.245.249.229:8080/api/1.0/login/ 
            -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq" 
            -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf" 
            -X POST
        
            [
                {
                    "hash_key": "23215634", 
                    "key": "455597c8-59b6-f6cc-a6ed-078986e819fb", 
                    "link_image": "http://abs.twimg.com/sticky/default_profile.png", 
                    "name": "Juan Mendoza", 
                    "nickname": "juanmen", 
                    "registered": "2014-05-21 02:53:55.791210", 
                    "score_answers": 0, 
                    "total_post": 0
                }
            ]
        '''
        
        args = self.parser.parse_args()
        user_tiwtter = twitter_credentials(args.access_token
                                                  ,args.token_secret 
                                                  ,g.tw_auth)
        #valida la respuesta dada por twitter.  
        if user_tiwtter.status == 200:
            datos = marshal(user_tiwtter.data, format_user_twitter)
            user = get_item(table, key_twitter = datos['key_twitter'])
            
            #Valida si el usuario ya se encuentra registrado en la base de datos.
            #si no existe se crea y si existe se actualiza.
            if user == None:
                datos['registered'] = timeUTCCreate()
                datos['key_user'] = hashCreate()
                user = Item(table, datos)
            else:
                user._data['nickname'] = datos['nickname']
                user._data['name'] = datos['name']
                user._data['link_image'] = datos['link_image']
                    
            user.save()
        else:
            abort(401)
        
        return [user._data]