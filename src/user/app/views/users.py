'''
Created on May 8, 2014

@author: anroco
'''

from boto.dynamodb2.items import Item
from flask.ext.restful import Resource, marshal_with, reqparse, marshal
from ..Common import timeUTCCreate, hashCreate, hashValidation, load_json, get_item
from ..app import dynamodb
from ..views.formats import format_user


db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_user']
parser = reqparse.RequestParser()

class User(Resource):
    
    decorators = [marshal_with(format_user(is_get=True))]
    
    parser.add_argument('id_t', type=str)
    parser.add_argument('data', type=load_json)
    
    from flask.ext.restful import types
    parser.add_argument('basic', type=types.boolean, default=False)
    
    
    def get(self):
        '''
        () -> list        
        
        requisito: *key_t* no None
        
        recibe las solicitudes GET del endpoint ('/user/'). Si el atributo 
        *basic* es true, retorna el usuario con los atributos basicos 
        definidos en la lista formats.BASIC_USER_FIELDS. Si es false retorna
        el usuario con todos los campos que este tiene.
        '''
        
        from .formats import BASIC_USER_FIELDS
        
        args = parser.parse_args()
        
        #valida el atributo *basic* para definir el tipo de consulta a realizar.
        if args.basic:
            result = table.get_item(key_twitter = args.id_t
                                    , attributes = BASIC_USER_FIELDS)
        else:
            result = table.get_item(key_twitter = args.id_t)
        return [result._data]
    
    
    def post(self):
        '''
        () -> list        
        
        requisito: *data* tiene formato json 
        
        recibe la solicitud POST del endpoint ('/user/') para regristrar 
        un usuario.
        
        El archivo json define el siguente formato base (puede tener mas 
        atributos):
        
        {
            'hash_key': value,
            'nickname': value,
            'name' : value,
            'link_image': value,
        }
        
        En caso de ser exitosa la creacion o si el usuario ya se encuentra 
        registrado en la base de datos se retorna un json con los datos del 
        usuario.
        
        Si el usuario ya esta registrado se actualizan los atributos 
        nickname, name y link_image    
        '''
        
        args = parser.parse_args()
        datos = marshal(args.data, format_user())
        new_item = get_item(table, key_twitter = datos['key_twitter'])
          
        #Valida si el usuario ya se encuentra registrado en la base de datos.
        if new_item == None:
            datos['registered'] = timeUTCCreate()
            datos['key_user'] = hashCreate()
            new_item = Item(table, datos)
        else:
            new_item._data['nickname'] = datos['nickname']
            new_item._data['name'] = datos['name']
            new_item._data['link_image'] = datos['link_image']

        new_item.save()       
        return [new_item._data]
    
    
    def put(self):
        '''
        () -> list        
        
        requisito: *data* tiene formato json 
        
        recibe la solicitud PUT del endpoint ('/user/') para actualizar los
        datos de un usuario registrado.
        
        El archivo json define el siguente formato base (puede tener mas 
        atributos):
        
        {
            'hash_key': value,
            'id' : value,
            'nickname': value,
            'name' : value,
            'link_image': value,            
        }
        
        En caso de ser exitosa la actualizacion se retorna un json con los 
        datos del usuario actualizado.
        '''
        
        args = parser.parse_args()
        datos = marshal(args.data, format_user())
        item = get_item(table, key_twitter = datos['key_twitter'])
        
        if item != None:
            item._data['nickname'] = datos['nickname']
            item._data['name'] = datos['name']
            item._data['link_image'] = datos['link_image']
            item._data['total_post'] = datos['total_post']
            item._data['score_answers'] = datos['score_answers']
            item.save()
            
        return [item._data]
        
        

class User_post(Resource):
    
    parser.add_argument('id_u', type=hashValidation)
    
    @marshal_with(format_user(is_get=True))
    def get(self):
        '''
        () -> list        
        
        requisito: key_u debe tener formato uuii(16)
        
        recibe las solicitudes GET del endpoint ('/post/user/')
        y retorna toda la informacion relacionada a ese usuario.
        '''
        
        args = parser.parse_args()
        result = table.query_2(key_user__eq = args.id_u, index = 'key_user_index')
        return [result.next()]
        