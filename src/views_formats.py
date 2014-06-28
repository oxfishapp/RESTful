# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

'''
Created on May 21, 2014

@author: root
'''
from flask.ext.restful import fields
from commons import Set_to_List, HashKey_Validation, Email_validation


#lista de campos a traer en una consulta a la tabla users
BASIC_USER_FIELDS = ['key_twitter', 'key_user'
                     , 'link_image', 'name', 'nickname']

#estructura de datos de usuario para el header.
format_user_header = {'token_user': fields.String
               , 'hash_key': fields.String(attribute='key_twitter')
               , 'key': HashKey_Validation(attribute='key_user')
               , 'link_image': fields.String
               , 'nickname': fields.String
               , 'skills': Set_to_List
               }

#estructura de datos usuario a ser retornados tras una solicitud a un recurso
format_user = {'hash_key': fields.String(attribute='key_twitter')
               , 'key': HashKey_Validation(attribute='key_user')
               , 'nickname': fields.String
               , 'name' : fields.String
               , 'email' : Email_validation
               , 'registered': fields.String
               , 'link_image': fields.String
               , 'total_post': fields.Integer
               , 'score_answers': fields.Integer
               , 'score_win_answers': fields.Integer
               , 'skills': Set_to_List
               }

#estructura de datos para mapear los datos de un usuario en
#formato twitter a la estuctura de la base de datos de la app.
format_user_twitter = {'key_twitter': fields.String(attribute='id_str')
                   , 'nickname': fields.String(attribute='screen_name')
                   , 'name' : fields.String
                   , 'link_image': fields.String(attribute='profile_image_url')
                   }

format_timeline= {'keys':
                      {
                      'hash_key': HashKey_Validation(attribute='key_post')
                      ,'hash_key_original': HashKey_Validation(attribute='key_post_original')
                      }
                   ,'geolocation': fields.String
                   ,'flag_answer': fields.Integer
                   ,'skills': Set_to_List
                   ,'key_timeline_post':fields.String
                   ,'key_user':HashKey_Validation
                   ,'message140':fields.String
                   ,'total_answers':fields.Integer
                   ,'win_answers':Set_to_List
                   ,'link':fields.String
                   ,'source':fields.String
                   ,'nickname':fields.String
                   ,'name':fields.String
                   ,'link_image':fields.String
                   ,'win':fields.Integer
                  }

# format_question={'Keys':
#                       {
#                       'HashKey': HashKey_Validation(attribute='Key_Post')
#                       ,'HashKeyOriginal': HashKey_Validation(attribute='Key_PostOriginal')
#                       }
#                    ,'Geolocation': fields.String
#                    ,'FlagAnswer': fields.Integer
#                    ,'Tags': Set_to_List
#                    ,'Key_TimelinePost':fields.String
#                    ,'Key_User':HashKey_Validation
#                    ,'Message140':fields.String
#                    ,'TotalAnswers':fields.Integer
#                    ,'WinAnswers':Set_to_List
#                    ,'Link':fields.String
#                    ,'Source':fields.String
#                   }
