# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask.ext.restful.fields import Raw
from boto.resultset import ResultSet

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
    usado en un batch_get de DynamoDB.
    
    >>> hashKeyList('["11EC2020-3AEA-4069-A2DD-08002B30309D"]')
    [{'Key_Post': u'11EC2020-3AEA-4069-A2DD-08002B30309D'}]
    >>> hashKeyList('["11EC2020-3AEA-4069-A2DD-08002B30309D","21EC2020-3AEA-4069-A2DD-08002B30309D"]')
    [{'Key_Post': u'11EC2020-3AEA-4069-A2DD-08002B30309D'}, {'Key_Post': u'21EC2020-3AEA-4069-A2DD-08002B30309D'}]
    
    """
    
    list_hashkey = []
    values = jsondecoder(value)
    for item in values:
        list_hashkey.append({'Key_Post': hashValidation(item)})
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
                result.append(dict(item))
        return result
    #print(value)
    result.append(items)
    return result
    
    
    