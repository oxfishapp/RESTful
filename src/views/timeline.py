# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from flask.ext.restful import Resource, reqparse, marshal_with
from formats import timeline_f
from commons import (hashKeyList 
                     , items_to_list 
                     , hashValidation
                     , jsondecoder
                     , hashCreate
                     , timeUTCCreate)

conn = DynamoDBConnection(  host='localhost'
                           ,port=8000
                           ,aws_access_key_id='DEVDB' #anything will do
                           ,aws_secret_access_key='DEVDB' #anything will do
                           ,is_secure=False)

timeline_t = Table('TimelineV14', connection=conn)

#Global All Index Timeline Public
class Timeline_Index(Resource):
    decorators = [marshal_with(timeline_f)]
    
    def get(self):
        """ () -> list
        
        Retorna la lista de preguntas en la vista
        Publica de Oxfish.  
        
        Example:
        
            curl http://localhost:5000/publictimeline
             
        """
        questions = timeline_t.query_2(FlagAnswer__eq=1
                                       ,limit=3
                                       ,index='GAI_TimelinePublic'
                                       ,reverse=True)
                #,exclusive_start_key=_exclusive_start_key
        return items_to_list(questions)
    
#Global All Index Home
class Timeline_Home_Index(Resource):
    decorators = [marshal_with(timeline_f)]
    
    def get(self, key):
        """ (str) -> list
        
        Retorna una lista con las preguntas realizadas
        por un usuario en particular.   
        
        Formato con el cual consulta en la tabla timeline
        para obtener el Home de un usuario en particular:
        
        key= 
            "str" -> UUID  
            
        Example:
            curl http://localhost:5000/home/<string:"UUID">     
        
        """
        homeUser = timeline_t.query_2(Key_User__eq=key
                                      ,limit=3
                                      ,index='GAI_Home'
                                      ,reverse=True)
        #,exclusive_start_key=_exclusive_start_key
        return items_to_list(homeUser)


class Timeline_Questions(Resource):
    decorators = [marshal_with(timeline_f)]
    
    def get(self, key):
        """ (str) -> list
        
        Retorna el encabezado (Pregunta) de una 
        vista en particular.
        
        Formato con el cual consulta en la tabla timeline
        para obtener una pregunta en particular:
        
        key= 
            "str" -> UUID  
            
        Example:
            curl http://localhost:5000/post_q/<string:"UUID">
        
        """
        header_q = timeline_t.get_item(Key_Post=hashValidation(key))
        
        return items_to_list(header_q._data)

#Batch Get Timeline Table
class Timeline_WinAnswers(Resource):
    decorators = [marshal_with(timeline_f)]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('HashKeyList', type=hashKeyList, required=True)
        super(Timeline_WinAnswers, self).__init__()
    
    def get(self):
        """ () -> list
        
        Retorna una lista con las respuestas ganadoras
        de una pregunta particular.
        
        Formato con el cual consulta en la tabla timeline
        para obtener la lista de respuestas ganadoras de 
        una pregunta:
        
        HashKeyList= 
            list["str","str"] -> "str" -> UUID  
            
        Example:
            
            curl http://localhost:5000/winanswers 
                -d 'HashKeyList=["UUID","UUID"]' 
                -X GET
        
        """
        args = self.reqparse.parse_args()
        hashkeylist = args.HashKeyList
        
        winAnswers = timeline_t.batch_get(hashkeylist)   
        
        return items_to_list(winAnswers)
 
 
class Timeline_Answers(Resource):
    decorators = [marshal_with(timeline_f)]  
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('HashKey', type=hashValidation, required=True)
        super(Timeline_Answers, self).__init__()  

    def get(self):
        """ (str) -> list
        
        Retorna una lista cronológica con las respuestas
        de una pregunta en particular para ser cargadas 
        en la vista aloneview.
        
        Formato con el cual consulta en la tabla timeline
        para obtener la lista de respuestas de una pregunta:
        
        HashKey= 
            "str" -> UUID  
        
        Example:
        
            curl http://localhost:5000/aloneview 
                -d 'HashKey=UUID' 
                -X GET
        
        """
        
        args = self.reqparse.parse_args()
        hashkey = args.HashKey
        
        answers = timeline_t.query_2(Key_PostOriginal__eq=hashkey
                                     ,limit=3
                                     ,index='GAI_VerTodoPublic'
                                     ,reverse=True)
        #,exclusive_start_key=_exclusive_start_key

        return items_to_list(answers)


class Timeline_Update(Resource):
     
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('HashKey', type=hashValidation, required=False)
        self.reqparse.add_argument('JsonTimeline', type=str, required=False)
        super(Timeline_Update, self).__init__()   
    
    @marshal_with(timeline_f)
    def post(self):
        """ () -> list
         
        Recibe por parse un string el cual es un 
        json encoder con los campos necesarios para 
        crear un nuevo registro en la tabla Timeline.  
        
        Se valida la existencia del key Key_PostOriginal
        en el diccionario para determinar si es
        pregunta o respuesta.
        
        Formato con el cual inserta el nuevo item
        en la tabla timeline:
        
        Insert Question
        JsonTimeline=
            {
                "Message140": str
                , "Source": str
                , "Geolocation": str -> Format = "4.598056,-74.075833"
                , "Tags": [,,]
                , "Link": str
                , "Key_User": "UUID"
            }
        
        Insert Answer
        JsonTimeline=
            {
                "Message140": str
                , "Source": str
                , "Geolocation": str -> Format = "4.598056,-74.075833"
                , "Link": "Imagen de Pregunta"
                , "Key_User": "UUID"
                , "Key_PostOriginal" : "UUID"
            }
        
        Examples:
        
            curl http://localhost:5000/post_q 
                -d 'JsonTimeline=
                                {
                                    "Message140": str
                                    , "Source": str
                                    , "Geolocation": str -> Format = "4.598056,-74.075833"
                                    , "Tags": [,,]
                                    , "Link": str
                                    , "Key_User": "UUID"
                                }'
                 -X POST
             
            curl http://localhost:5000/post_a 
                -d 'JsonTimeline=
                                {
                                    "Message140": str
                                    , "Source": str
                                    , "Geolocation": str -> Format = "4.598056,-74.075833"
                                    , "Link": "Imagen de Pregunta"
                                    , "Key_User": "UUID"
                                    , "Key_PostOriginal" : "UUID"
                                }' 
                -X POST
        
        """
        
        args = self.reqparse.parse_args()
        posting = jsondecoder(args.JsonTimeline)
        
        posting['Key_Post'] = hashCreate()
        posting['Key_TimelinePost'] = timeUTCCreate()
        
        if not posting.get('Key_PostOriginal'):
            posting['FlagAnswer'] = 0
            posting['Tags'] = set(posting['Tags'])
        
        from boto.dynamodb2.items import Item
        item = Item(timeline_t, posting)
        item.save()
        
        return items_to_list(posting)


    def put(self):
        """ () -> list
         
        Recibe por parser un string el cual es un
        json encoder con los campos necesarios para 
        actualizar un registro en particular en la 
        tabla Timeline   
        
        Formato con el cual actualiza los atributos
        en la tabla timeline:
        
        JsonTimeline=
            {
               "TotalAnswers" : int -> 1 sum 0 same
               ,"WinAnswers" : {
                                "State" : int -> 1 add 0 remove
                                ,"HashKey" : "str" -> UUID
                                }
            }    
        
        HashKey= 
            "str" -> UUID  
        
        Examples:
        
        curl http://localhost:5000/update 
            -d 'HashKey=UUID' 
            -d 'JsonTimeline={"TotalAnswers" : int}' 
            -X PUT
            
        curl http://localhost:5000/update 
            -d 'HashKey=UUID' 
            -d 'JsonTimeline={"WinAnswers" : {
                                                "State" : int, 
                                                "HashKey" : "UUID"
                                              }
                              }' 
            -X PUT
        """
        args = self.reqparse.parse_args()
        attributes = jsondecoder(args.JsonTimeline)
        hashKey = args.HashKey
        
        item = timeline_t.get_item(Key_Post=hashKey)
        item._data['FlagAnswer'] = 1
        
        if attributes.get('TotalAnswers'):
            if item._data.get('TotalAnswers'):
                item._data['TotalAnswers'] += 1
            else:
                item._data['TotalAnswers'] = 1

        if attributes.get('WinAnswers'):
            if item._data.get('WinAnswers'):
                if attributes['WinAnswers']["State"]:
                    item._data['WinAnswers'].add(attributes['WinAnswers']["HashKey"])
                else:
                    item._data['WinAnswers'].remove(attributes['WinAnswers']["HashKey"])
            else:
                item._data['WinAnswers'] = set([attributes['WinAnswers']["HashKey"]])
        
        item.save()
        
        return 'Actualizado'
     
    def delete(self):
        """ () -> list
         
        Recibe por parser un string el cual es un
        json encoder con los campos necesarios para 
        eliminar un registro en particular en la 
        tabla Timeline. 
         
        Se podrá eliminar una pregunta si y solo si 
        no tiene respuestas ya realizadas asociadas a 
        dicha pregunta.
         
        Se podrá eliminar una respuesta si y solo si
        no es una respuesta ganadora o winanswer de la 
        pregunta a la que esta haciendo referencia.   
        
        Retornara tres valores diferentes:
        
            1. Si se elimina una Pregunta retornara al home
                del usuario
            2. Si se elimina una Respuesta retornara al aloneview
                de la pregunta original.
            3. Si no es posible eliminar, la pregunta o la
                respuesta retornara una vista que diga.
                No puedes eliminar este item.
                
        Estas validaciones se deberan realizar en el frontend
        con javascript.
        
        Formato con el cual elimina un item 
        en la tabla timeline:
        
        HashKey= 
            "str" -> UUID  
            
        Examples:
        
        curl http://localhost:5000/delete 
            -d 'HashKey=UUID' 
            -X DELETE -v 
            
        """
        
        args = self.reqparse.parse_args()
        hashKey = args.HashKey
        
        deleteItem = timeline_t.get_item(Key_Post=hashKey)
        deleteItem.delete()
        
        return 'Eliminado'
        
        
    
    
    