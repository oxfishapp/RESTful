# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask.ext.restful.fields import Raw

class Set_to_List(Raw):
    def format(self, value):
        """ (set) -> list
        
        Convertir un set a list y retornarlo.
        
        """
        
        return list(value)
    
class HashKey_Validation(Raw):
    def format(self, value): 
        """ (str) -> str
        
        Valida que el HashKey tenga un formato consistente
        con UUID.
        
        """
        
        return hashValidation(value)

def hashValidation(value):
    """ (str) -> str
    
    Recibe un string el cual es un UUID se valida
    si su formato es correcto, de ser así se retorna 
    el string, de lo contrario se retorna un error.
    
    >>> hashValidation('d6df4adc-b533-9545-9d61-7c877bb53b18')
    'd6df4adc-b533-9545-9d61-7c877bb53b18'
    >>> hashValidation('d6df4adc-b533-9545-9d61-7c877bb53b1')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 12, in hashValidation
    NameError: Hash Validation Crash
    
    """
    
    import re
    regex = re.compile('[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z', re.I)
    boolhash = regex.match(value)
    if bool(boolhash):
        return value
    #Genera error
    raise NameError('Hash Validation Crash')

def hashCreate():
    """ () -> str
    
    Retorna un string el cual es un UUID.
    
    >>> hashCreate()
    'd6df4adc-b533-9545-9d61-7c877bb53b18'
    
    """
    
    import uuid, M2Crypto
    value = uuid.UUID(bytes = M2Crypto.m2.rand_bytes(16))
    return str(value)

def hashKeyList(value):
    """ (str) -> list
    
    Recibe un string el cual es un json encoder 
    y retorna una lista de diccionarios para ser
    usado en un batch_get de dynamoDB.
    
    >>> hashKeyList('["11EC2020-3AEA-4069-A2DD-08002B30309D"]')
    [{'Key_Post': u'11EC2020-3AEA-4069-A2DD-08002B30309D'}]
    >>> hashKeyList('["11EC2020-3AEA-4069-A2DD-08002B30309D","21EC2020-3AEA-4069-A2DD-08002B30309D"]')
    [{'Key_Post': u'11EC2020-3AEA-4069-A2DD-08002B30309D'}, {'Key_Post': u'21EC2020-3AEA-4069-A2DD-08002B30309D'}]
    
    """
    
    list_hashkey = []
    values = jsondecoder(value)
    for item in values:
        list_hashkey.append({'key_post': hashValidation(item)})
    return list_hashkey

def jsondecoder(encoder):
    """ (str) -> json_decoder
    
    Recibe un string el cual es un json encoder 
    y retorna un json decoder
    
    >>> jsondecoder('{"Key" : "zxc-123"}')
    {u'Key': u'zxc-123'}
    >>> jsondecoder('{"Key" : "abcd-1234", "List" : [0,1,2,3]}')
    {u'List': [0, 1, 2, 3], u'Key': u'abcd-1234'}
    
    """
    
    import json
    values = json.loads(encoder)
    return values

def timeUTCCreate():
    """ () -> str
    
    Retorna un string con la fecha actual en UTC Z.
    
    >>> timeUTCCreate()
    '2014-05-15 19:01:47.669254'
    
    """
    
    from datetime import datetime
    return str(datetime.utcnow())

#Post
#Respuestas
def items_to_list(items):
    """ (items) -> list
    
    Recibe un ResultSet o un Diccionario y 
    Retorna una lista de diccionarios.
    
    >>> items_to_list({1:1})
    [{1:1}]
    
    """
        
    result = []
    
    from boto.dynamodb2.results import ResultSet
    if isinstance(items, ResultSet):
        for item in items:
                result.append(item_to_dict(item._data))
        return result
    #print(value)
    result.append(items)
    return result

def item_to_dict(value):
    
    dict = {}
    dict.update(value)
    
    from application import dynamodb
    table = dynamodb.tables['tbl_user']
    
    user_insert = table.query_2(key_user__eq = value['key_user'], index = 'key_user_index').next()
    
    dict.update(user_insert)
    
    return dict


def get_item(table, **kwargs):
    '''
    (boto.dynamodb2.table.Table, **kwarg) -> boto.dynamodb2.items.Item
    
    retorna un item de la tabla 'table' buscado por hash_key y/o range_key
    si no se encuentra un item retorna None
    
    Ejemplo::

        Con solo hash key.    
        get_item(table=user, key_user='1234')
            
        Con hash + range key.
        get_item(table=user, key_user='1234', username='pepito')
    '''
    
    from boto.dynamodb2.exceptions import ItemNotFound
    from boto.exception import JSONResponseError
         
    try:
        item = table.get_item(**kwargs)
    except (ItemNotFound, JSONResponseError):
        return None

    return item


def twitter_credentials(access_token, token_secret, tw_auth):
    '''
    (str, str, flask_oauth.OAuth) -> 
    
    Valida si el access_token y token_secret del usuario son validos, retorna 
    un json con los datos del usuario el cual es suministrado por los servicios 
    de twitter y un status 200, en caso contrario retorna un mensaje de error y
    status 401.
    '''
    
    #definicion de una funcion tokengetter necesaria para el funcionamiento de 
    #Flask-Oauth retorna una tubla con los valores del access_token y token_secret
    def get_twitter_token(token = access_token, secret = token_secret):
        return token, secret
    
    tw_auth.tokengetter(get_twitter_token)    
    return tw_auth.get('account/verify_credentials.json')
    

class email_validation(Raw):
    def format(self, value): 
        """ (str) -> str
        
        Verifica que value tiene la estructura de un email
        """
        
        return validate_email(value)

def validate_email(email):
    """ (str) -> boolean
    
    Permite verificar que el email proporcionado tiene el formato adecuado 
    Si correcto retorna el email de lo contrario lanza un NameError.    
    """
    
    import re
    result = re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$'
                      ,email.lower())
    if result:
        return email
    raise NameError('Malformed email')