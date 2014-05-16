'''
Created on May 14, 2014

@author: anroco
'''

from flask.ext.restful import fields


#lista de campos a traer en una consulta a la tabla users
BASIC_USER_FIELDS = ['key_twitter','key_user','link_image','name','nickname']

def format_user(is_get=False):
    if is_get: field = [['hash_key','key_twitter'],['id','key_user']]
    else: field = [['key_twitter','hash_key'],['key_user','id']]
    
    format_user = {field[0][0]: fields.String(attribute=field[0][1])
                   ,field[1][0]: fields.String(attribute=field[1][1])
                   ,'nickname': fields.String
                   ,'name' : fields.String
                   ,'registered': fields.String
                   ,'link_image': fields.String
                   ,'total_post': fields.Integer
                   ,'score_answers': fields.Integer
                   }
    return format_user
        

