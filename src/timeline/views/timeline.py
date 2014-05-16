# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from flask.ext.restful import Resource, reqparse, marshal_with
from timeline.commons import ( hashKeyList 
                             , items_to_list 
                             , hashValidation
                             , jsondecoder
                             , hashCreate
                             , timeUTCCreate)
from timeline.formats import timeline_f

conn = DynamoDBConnection(
    host                    =   'localhost'
   ,port                    =   8000
   ,aws_access_key_id       =   'DEVDB' #anything will do
   ,aws_secret_access_key   =   'DEVDB' #anything will do
   ,is_secure               =   False
                        )
timeline_t = Table('TimelineV14', connection=conn)

#Global All Index Timeline Public
class Timeline_Index(Resource):
    decorators = [marshal_with(timeline_f)]
    
    def get(self):
        """ () -> list
        
        Retorna la lista de preguntas en la vista
        Publica de Oxfish.  
             
        """
        questions = timeline_t.query_2(FlagAnswer__eq=1
                                  ,limit=20
                                  ,index='GAI_TimelinePublic')
                #,exclusive_start_key=_exclusive_start_key
        return items_to_list(questions)
    
#Global All Index VerTodoPublic
class AloneView_Index(Resource):
    decorators = [marshal_with(timeline_f)]    

    def get(self, key):
        """ (str) -> list
        
        Retorna las respuestas de una pregunta en 
        particular.
        
        """
        answers = timeline_t.query_2(
                         Key_PostOriginal__eq=key
                        ,limit=20
                        ,index='GAI_VerTodoPublic'
               #,exclusive_start_key=_exclusive_start_key
               )
   
        return items_to_list(answers)

#Global All Index Home
class Home_Index(Resource):
    decorators = [marshal_with(timeline_f)]
    
    def get(self, key):
        """ (str) -> list
        
        Retorna una lista con las preguntas realizadas
        por un usuario en particular.        
        
        """
        homeUser = timeline_t.query_2(Key_User__eq=key
                                      ,limit=20
                                      ,index='GAI_Home')
        #,exclusive_start_key=_exclusive_start_key
        return items_to_list(homeUser)

class Timeline_Questions(Resource):
    decorators = [marshal_with(timeline_f)]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('JsonTimeline', type=str, required=True)
        super(Timeline_Questions, self).__init__()
    
    def get(self, key):
        """ (str) -> list
        
        Retorna el encabezado (Pregunta) de una 
        vista en particular.
        
        """
        
        header = timeline_t.get_item(Key_Post=hashValidation(key))
        
        return items_to_list(header._data)
    
    def post(self):
        """ () -> list
        
        Recibe por parse un string el cual es un 
        json encoder con los campos necesarios para 
        crear un nuevo registro en la tabla Timeline.  
        
        """
        
        args = self.reqparse.parse_args()
        posting = jsondecoder(args.JsonTimeline)
        
        posting['Key_Post'] = hashCreate()
        posting['Key_TimelinePost'] = timeUTCCreate()
        posting['FlagAnswer'] = 0
        posting['Tags'] = set(posting['Tags'])
        
        from boto.dynamodb2.items import Item
        item = Item(timeline_f, posting)
        item.save()
        
        return items_to_list(posting)

#Batch Get Timeline Table
class Timeline_WinAnswers(Resource):
    decorators = [marshal_with(timeline_f)]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('HashKeyList', type=hashKeyList, default=None, required=False)
        super(Timeline_WinAnswers, self).__init__()
    
    def get(self):
        """ () -> list
        
        Retorna una lista con las respuestas ganadoras
        de una pregunta particular.
        
        """
        args = self.reqparse.parse_args()
        hashkeylist = args.HashKeyList
        
        winAnswers = timeline_t.batch_get(hashkeylist)   
        
        return items_to_list(winAnswers)
# 
# class Timeline_Answers(Resource):
#         
#     def get(self):
#         """ () -> list
#         
#         Retorna una lista cronologica con las respuetas
#         de una pregunta en particular para ser cargadas 
#         en la vista aloneview.
#         
#         """
#         pass
#         
#     def post(self):
#         """ () -> list
#         
#         Recibe por parse un string el cual es un 
#         json encoder con los campos necesarios para 
#         crear un nuevo registro en la tabla Timeline.  
#         
#         """
#         
#         pass
#         
# class Timeline_Update_Questions(Resource):
#     
#     def put(self):
#         """ () -> list
#         
#         Recibe por parser un string el cual es un
#         json encoder con los campos necesarios para 
#         actualizar un registro en particular en la 
#         tabla Timeline        
#         
#         """
#         pass
#     
#     def delete(self):
#         """ () -> list
#         
#         Recibe por parser un string el cual es un
#         json encoder con los campos necesarios para 
#         eliminar un registro en particular en la 
#         tabla Timeline. 
#         
#         Se podra eliiminar una pregunta si y solo si 
#         no tiene respuestas ya realizadas asociadas a 
#         dicha pregunta.
#         
#         Se podra eliminar una respuesta si y solo si
#         no es una respuesta ganadora o winanswer de la 
#         pregunta a la que esta haciendo regeferencia.     
#         
#         """
#         pass
#     
#     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
    