'''
Created on May 15, 2014

@author: anroco
'''

def hashValidation(*args, **kw_args):
    import re
    value = args[0].encode('utf-8')
    regex = re.compile('[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z', re.I)
    boolhash = regex.match(value)
    if bool(boolhash):
        return value
    #Genera error
    raise NameError('Hash Validation Crash')


def hashCreate(num_bytes=16):
    import uuid, M2Crypto
    value = uuid.UUID(bytes = M2Crypto.m2.rand_bytes(num_bytes))
    return str(value)


def timeUTCCreate():
    from datetime import datetime
    datetime.utcnow()
    return str(datetime.utcnow())

def resultSet_to_list(resultSet):
    result = []
    for item in resultSet:
            result.append(dict(item))
    return result

def load_json(value):
    '''
    () -> json
    
    retorna la informacion en formato json que se encuentra en la varible value
    si los datos contenidos en value no son json se genera una excepcion.
    '''
    import json
    return json.loads(value)


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
