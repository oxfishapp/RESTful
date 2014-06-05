'''
Created on May 8, 2014

@author: anroco
'''
from functools import wraps
from flask import abort
from boto.dynamodb2.exceptions import ItemNotFound


def error_handled(f):
    @wraps(f)
    def exceptions(*args, **kw_args):
        try:
            return f(*args, **kw_args)
        except (StopIteration, ItemNotFound):
            abort(404)
        except ValueError as e:
            abort(404, e.message)
    return exceptions
