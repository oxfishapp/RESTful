'''
Created on May 14, 2014

@author: anroco
'''

from flask.ext.restful import fields


#lista de campos a traer en una consulta a la tabla users
BASIC_USER_FIELDS = ['key_twitter','key_user','link_image','name','nickname']

#estructura de datos de usuario a ser retornados tras una solicitud a un recurso user
format_user = {'hash_key': fields.String(attribute='key_twitter')
               ,'id': fields.String(attribute='key_user')
               ,'nickname': fields.String
               ,'name' : fields.String
               ,'registered': fields.String
               ,'link_image': fields.String
               ,'total_post': fields.Integer
               ,'score_answers': fields.Integer
               }

#estructura de datos para mapear los datos de un usuario en formato twitter a 
#la estuctura de la base de datos de la app.
format_user_twitter = {'key_twitter': fields.String(attribute='id_str')
                   ,'key_user': fields.String
                   ,'nickname': fields.String(attribute='screen_name')
                   ,'name' : fields.String
                   ,'registered': fields.String
                   ,'link_image': fields.String(attribute='profile_image_url')
                   ,'total_post': fields.Integer
                   ,'score_answers': fields.Integer
                   }

