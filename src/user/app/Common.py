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
    import json
    return json.loads(value)

def get_item(table, **kwargs):
    from boto.dynamodb2.exceptions import ItemNotFound
    from boto.exception import JSONResponseError
         
    try:
        item = table.get_item(**kwargs)
    except (ItemNotFound, JSONResponseError):
        return None

    return item
