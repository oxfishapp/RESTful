# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from application import dynamodb
from flask.ext.restful import Resource, reqparse, marshal_with
from formats import format_timeline
from commons import (  hashKeyList 
                     , items_to_list 
                     , hashValidation
                     , jsondecoder
                     , hashCreate
                     , timeUTCCreate)

db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_timeline']

#Global All Index Timeline Public
class Timeline_Index(Resource):
    decorators = [marshal_with(format_timeline)]
    
    def get(self):
        """ () -> list
        
        Retorna la lista de preguntas en la vista
        Publica de Oxfish.  
        
        Example:
        
            curl http://localhost:5000/api/1.0/publictimeline
             
        """
        
        a = table.scan()
        
        a
       
        questions = table.query_2(flag_answer__eq=0
                                       ,limit=3
                                       ,index='GAI_TimelinePublic'
                                       ,reverse=True)
                #,exclusive_start_key=_exclusive_start_key
        return items_to_list(questions)
    
#Global All Index Home
class Timeline_Home_Index(Resource):
    decorators = [marshal_with(format_timeline)]
    
    def get(self, key):
        """ (str) -> list
        
        Retorna una lista con las preguntas realizadas
        por un usuario en particular.   
        
        Formato con el cual consulta en la tabla timeline
        para obtener el Home de un usuario en particular:
        
        key= 
            "str" -> UUID  
            
        Example:
            curl http://localhost:5000/api/1.0/home/87654321-e9f0-69cc-1c68-362d8f5164ea">     
        
        """
        homeUser = table.query_2(key_user__eq=key
                                      ,limit=3
                                      ,index='GAI_Home'
                                      ,reverse=True)
        #,exclusive_start_key=_exclusive_start_key
        return items_to_list(homeUser)


class Timeline_Questions(Resource):
    decorators = [marshal_with(format_timeline)]
    
    def get(self, key):
        """ (str) -> list
        
        Retorna el encabezado (Pregunta) de una 
        vista en particular.
        
        Formato con el cual consulta en la tabla timeline
        para obtener una pregunta en particular:
        
        key= 
            "str" -> UUID  
            
        Example:
            curl http://localhost:5000/api/1.0/post_q/11EC2020-3AEA-4069-A2DD-08002B30309D">
        
        """
        header_q = table.get_item(key_post=hashValidation(key))
        
        return items_to_list(header_q._data)

#Batch Get Timeline Table
class Timeline_win_answers(Resource):
    decorators = [marshal_with(format_timeline)]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hash_keyList', type=hashKeyList, required=True)
        super(Timeline_win_answers, self).__init__()
    
    def get(self):
        """ () -> list
        
        Retorna una lista con las respuestas ganadoras
        de una pregunta particular.
        
        Formato con el cual consulta en la tabla timeline
        para obtener la lista de respuestas ganadoras de 
        una pregunta:
        
        hash_keyList= 
            list["str","str"] -> "str" -> UUID  
            
        Example:
            
            curl http://localhost:5000/api/1.0/winanswers -d 'hash_keyList=["31EC2020-3AEA-4069-A2DD-08002B30309D","21EC2020-3AEA-4069-A2DD-08002B30309D"]' -X GET
        
        """
        args = self.reqparse.parse_args()
        hash_keylist = args.hash_keyList
        
        win_answers = table.batch_get(hash_keylist)   
        
        return items_to_list(win_answers)
 
 
class Timeline_Answers(Resource):
    decorators = [marshal_with(format_timeline)]  
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hash_key', type=hashValidation, required=True)
        super(Timeline_Answers, self).__init__()  

    def get(self):
        """ (str) -> list
        
        Retorna una lista cronológica con las respuestas
        de una pregunta en particular para ser cargadas 
        en la vista aloneview.
        
        Formato con el cual consulta en la tabla timeline
        para obtener la lista de respuestas de una pregunta:
        
        hash_key= 
            "str" -> UUID  
        
        Example:
        
            curl http://localhost:5000/api/1.0/aloneview -d 'hash_key=11EC2020-3AEA-4069-A2DD-08002B30309D' -X GET
        
        """
        
        args = self.reqparse.parse_args()
        hash_key = args.hash_key
        
        answers = table.query_2(key_post_original__eq=hash_key
                                     ,limit=3
                                     ,index='GAI_VerTodoPublic'
                                     ,reverse=True)
        #,exclusive_start_key=_exclusive_start_key

        return items_to_list(answers)


class Timeline_Update(Resource):
     
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hash_key', type=hashValidation, required=False)
        self.reqparse.add_argument('jsontimeline', type=str, required=False)
        super(Timeline_Update, self).__init__()   
    
    @marshal_with(format_timeline)
    def post(self):
        """ () -> list
         
        Recibe por parse un string el cual es un 
        json encoder con los campos necesarios para 
        crear un nuevo registro en la tabla Timeline.  
        
        Se valida la existencia del key key_post_original
        en el diccionario para determinar si es
        pregunta o respuesta.
        
        Formato con el cual inserta el nuevo item
        en la tabla timeline:
        
        Insert Question
        jsontimeline=
            {
                "message140": str
                , "source": str
                , "geolocation": str -> Format = "4.598056,-74.075833"
                , "skills": [,,]
                , "link": str
                , "key_user": "UUID"
            }
        
        Insert Answer
        jsontimeline=
            {
                "message140": str
                , "source": str
                , "geolocation": str -> Format = "4.598056,-74.075833"
                , "link": "Imagen de Pregunta"
                , "key_user": "UUID"
                , "key_post_original" : "UUID"
            }
        
        Examples:
        
            curl http://localhost:5000/api/1.0/post_q 
                -d 'jsontimeline=
                                {
                                    "message140": str
                                    , "source": str
                                    , "geolocation": str -> Format = "4.598056,-74.075833"
                                    , "skills": [,,]
                                    , "link": str
                                    , "key_user": "UUID"
                                }'
                 -X POST
             
            curl http://localhost:5000/api/1.0/post_a 
                -d 'jsontimeline=
                                {
                                    "message140": str
                                    , "source": str
                                    , "geolocation": str -> Format = "4.598056,-74.075833"
                                    , "link": "Imagen de Pregunta"
                                    , "key_user": "UUID"
                                    , "key_post_original" : "UUID"
                                }' 
                -X POST
        
        """
        
        args = self.reqparse.parse_args()
        posting = jsondecoder(args.jsontimeline)
        
        posting['key_post'] = hashCreate()
        posting['key_timeline_post'] = timeUTCCreate()
        
        if not posting.get('key_post_original'):
            posting['flag_answer'] = 0
            posting['skills'] = set(posting['skills'])
        
        from boto.dynamodb2.items import Item
        item = Item(table, posting)
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
        
        jsontimeline=
            {
               "total_answers" : int -> 1 sum 0 same
               ,"win_answers" : {
                                "state" : int -> 1 add 0 remove
                                ,"hash_key" : "str" -> UUID
                                }
            }    
        
        hash_key= 
            "str" -> UUID  
        
        Examples:
        
        curl http://localhost:5000/api/1.0/update 
            -d 'hash_key=UUID' 
            -d 'jsontimeline={"total_answers" : int}' 
            -X PUT
            
        curl http://localhost:5000/api/1.0/update 
            -d 'hash_key=UUID' 
            -d 'jsontimeline={"win_answers" : {
                                                "state" : int, 
                                                "hash_key" : "UUID"
                                              }
                              }' 
            -X PUT
        """
        args = self.reqparse.parse_args()
        attributes = jsondecoder(args.jsontimeline)
        hash_key = args.hash_key
        
        item = table.get_item(key_post=hash_key)
        item._data['flag_answer'] = 1
        
        if attributes.get('total_answers'):
            if item._data.get('total_answers'):
                item._data['total_answers'] += 1
            else:
                item._data['total_answers'] = 1

        if attributes.get('win_answers'):
            if item._data.get('win_answers'):
                if attributes['win_answers']["state"]:
                    item._data['win_answers'].add(attributes['win_answers']["hash_key"])
                else:
                    item._data['win_answers'].remove(attributes['win_answers']["hash_key"])
            else:
                item._data['win_answers'] = set([attributes['win_answers']["hash_key"]])
        
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
        
        hash_key= 
            "str" -> UUID  
            
        Examples:
        
        curl http://localhost:5000/api/1.0/delete 
            -d 'hash_key=UUID' 
            -X DELETE -v 
            
        """
        
        args = self.reqparse.parse_args()
        hash_key = args.hash_key
        
        deleteItem = table.get_item(key_post=hash_key)
        deleteItem.delete()
        
        return 'Eliminado'
        
        
    
    
    
