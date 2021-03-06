# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask.ext.restful.fields import Raw
from api_errors import error_handled


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

    from flask import abort
    import re
    regex = re.compile('[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z', re.I)
    boolhash = regex.match(value)
    if bool(boolhash):
        return value
    #Genera error
    abort(400)

def hashCreate():
    """ () -> str

    Retorna un string el cual es un UUID.

    >>> hashCreate()
    'd6df4adc-b533-9545-9d61-7c877bb53b18'

    """

    import uuid

    value = uuid.uuid4()
    return str(value)

def pagination(data, value):
    
    _return = dict()
    _return['data'] = data
    
    if value:
        _return['pagination'] = value
    else:
        _return['pagination'] = None
            
    return _return

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
    #values = jsondecoder(value)
    for item in value:
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

    from dynamoDBqueries import User

    user = User()
    dictionary = {}
    dictionary.update(value)
    user_insert = user.get_by_key_user(value['key_user'])
    dictionary.update(user_insert)
    return dictionary


def twitter_credentials(access_token, token_secret):
    '''
    (str, str) -> dict

    Valida si el access_token y token_secret del usuario son validos, retorna
    un json con los datos del usuario el cual es suministrado por los servicios
    de twitter y un status 200, en caso contrario retorna un mensaje de error y
    status 401.
    '''

    from flask import current_app
    from flask_oauth import OAuth

    config = current_app.config

    tw_auth = OAuth().remote_app(name=config['TW_NAME'],
                            base_url=config['TW_BASE_URL'],
                            request_token_url=config['TW_REQUEST_TOKEN_URL'],
                            access_token_url=config['TW_ACCESS_TOKEN_URL'],
                            authorize_url=config['TW_AUTHORIZE_URL'],
                            consumer_key=config['TW_CONSUMER_KEY'],
                            consumer_secret=config['TW_CONSUMER_SECRET'])

    #definicion de una funcion tokengetter necesaria para el funcionamiento de
    #Flask-Oauth retorna una tubla con el access_token y token_secret
    def get_twitter_token(token=access_token, secret=token_secret):
        return token, secret

    tw_auth.tokengetter(get_twitter_token)
    return tw_auth.get('account/verify_credentials.json')


def validate_user_auth(token):
    '''
    (str) -> boto.dynamodb2.items.Item

    Valida si el token proporcionado es el mismos que tiene regitrado el
    usuadio en la base de datos. En caso de ser correcta la validacion se
    retorna el usuario y en caso de ser fallida retorna un status_code 401.
    '''

    from dynamoDBqueries import User
    from flask import abort

    user = User()
    token_user = decrypt_token(token)
    user = user.get_item(key_twitter=token_user['hash_key'])

    #valida si el usuario esta registrado en la base de datos y el token
    #proporcionado es igual al registrado en la base de datos.
    if user and token == user._data['token_user']:
        return user
    abort(401)


def decrypt_token(token_user, secret_key=None):
    '''
    (str) -> dict

    Permite verificar si el token_user es valido. En caso de ser valido es
    retornado un dict con los datos encriptados en el token, en caso de fallar
    la verificacion retorna None.

    Si el secret_key es None, se toma como valor por defecto el OX_SECRET_KEY
    defenido en la configuracion de la aplicacion para el proceso de cifrado y
    descifrado el token.

    JSON Web Token (JWT)
    '''

    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    from flask import current_app, abort

    if not secret_key:
        secret_key = current_app.config['OX_SECRET_KEY']
    token = Serializer(secret_key)
    try:
        data = token.loads(token_user)
    except:
        abort(401)
    return data


def generate_token(secret_key=None, expiration=0, **kwargs):
    '''
    (int, str, **kwargs) -> str

    Permite generar un token_user temporal en el cual se encapsularan y
    encriptaran los datos contenidos en el kwargs. Retorna un str con el
    token_user con los datos encriptados.

    Si el secret_key es None, se toma como valor por defecto el OX_SECRET_KEY
    defenido en la configuracion de la aplicacion para el proceso de cifrado y
    descifrado el token.

    JSON Web Token (JWT)
    '''

    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    from flask import current_app

    if not expiration:
        expiration = current_app.config['OX_TOKEN_USER_LIFETIME']
    if not secret_key:
        secret_key = current_app.config['OX_SECRET_KEY']
    token = Serializer(secret_key, expires_in=expiration)
    return token.dumps(kwargs)


class Email_validation(Raw):
    def format(self, value):
        """ (str) -> str

        Verifica que value tiene la estructura de un email

        Valido: juanperez@dominio.com
        Errado: juanperez@dominio@com
        """

        return validate_email(value)


#@error_handled
def validate_email(email):
    """ (str) -> boolean

    Permite verificar que el email proporcionado tiene el formato adecuado.
    Si es correcto retorna el email de lo contrario lanza un NameError.
    """

    from flask import abort
    import re
    result = re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                      email.lower())
    if result:
        return email
    abort(400)
#    raise ValueError('Malformed email')


def manage_score(score, action=0, points=1):
    '''
    (int, int, int) -> int

    Gestiona las acciones sobre un marcador, permite agregar o quitar points a
    un score, el tipo de accion a realizar sobre score se definen como sigue:

        * action=1 : se agrega la cantidad de points al score actual.
        * action=-1 : se quita la cantidad de points al score actual.

    Al finalizar la gestion del score se retorna el nuevo score con el tipo de
    accion realizada. Si action tiene cualquier otro valor a los definidos
    anteriormente se retorna el score sin modificaciones.
    '''

    new_score = score
    if action == 1:
        new_score += points
    if action == -1:
        new_score -= points
    return new_score if new_score >= 0 else score
