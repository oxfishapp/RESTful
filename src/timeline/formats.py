from flask.ext.restful import fields
from factory import hashValidation

class Set_to_List(fields.Raw):
    def format(self, value):
        return list(value)
    
class HashKey_Validation(fields.Raw):
    def format(self, value): 
        return hashValidation(value)

timeline= {
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