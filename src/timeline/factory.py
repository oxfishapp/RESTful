'''
Created on May 8, 2014

@author: root
'''
def hashValidation(value):
    import re
    regex = re.compile('[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z', re.I)
    boolhash = regex.match(value)
    if bool(boolhash):
        return value
    #Genera error
    raise NameError('Hash Validation Crash')

def hashCreate(num_bytes):
    import uuid, M2Crypto
    value = uuid.UUID(bytes = M2Crypto.m2.rand_bytes(num_bytes))
    return str(value)

def hashKeyList(value):
    import json
    list_hashkey = []
    values = json.loads(value)
    for item in values:
        list_hashkey.append({'Key_Post': hashValidation(item)})
    return list_hashkey

def timeUTCCreate():
    from datetime import datetime
    datetime.utcnow()
    return str(datetime.utcnow())

def resultSet_to_list(resultSet):
    result = []
    for item in resultSet:
            result.append(dict(item))
    return result