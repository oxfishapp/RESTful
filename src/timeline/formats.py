# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask.ext.restful import fields
from commons import Set_to_List, HashKey_Validation

timeline_f= {
          'Keys':
              {
              'HashKey': HashKey_Validation(attribute='Key_Post')
              ,'HashKeyOriginal': HashKey_Validation(attribute='Key_PostOriginal')
              }
           ,'Geolocation': fields.String
           ,'FlagAnswer': fields.Integer
           ,'Tags': Set_to_List
           ,'Key_TimelinePost':fields.String
           ,'Key_User':HashKey_Validation
           ,'Message140':fields.String
           ,'TotalAnswers':fields.Integer
           ,'WinAnswers':Set_to_List
           ,'Link':fields.String
           ,'Source':fields.String
          }