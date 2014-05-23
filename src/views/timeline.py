# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from application import dynamodb
from flask.ext.restful import Resource, reqparse, marshal_with, marshal
from formats import format_timeline
from commons import *
#from boto.dynamodb2.layer1 import DynamoDBConnection #DynamoDB Conexion

db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_timeline']

#Conexion
# table = DynamoDBConnection(
#     host='localhost',
#     port=8000,
#     aws_access_key_id='DEVDB', #anything will do
#     aws_secret_access_key='DEVDB', #anything will do
#     is_secure=False)

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
        questions = table.query_2(flag_answer__eq='True'
                                       ,limit=3
                                       ,index='TimelinePublic'
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
            curl http://localhost:5000/api/1.0/home/87654321-e9f0-69cc-1c68-362d8f5164ea
        
        """
        homeUser = table.query_2(key_user__eq=key
                                      ,limit=3
                                      ,index='Home'
                                      ,reverse=True)
        #,exclusive_start_key=_exclusive_start_key
        return items_to_list(homeUser)


class Timeline_QandWinA(Resource):
    #decorators = [marshal_with(format_timeline)]
    
    def get(self, key):
        """ (str) -> list
        
        Retorna el encabezado (Pregunta) de una 
        vista en particular con sus win answers 
        asociadas.
        
        Formato con el cual consulta en la tabla timeline
        para obtener una pregunta y sus win answers 
        en particular:
        
        key= 
            "str" -> UUID  
            
        Example:
            curl http://localhost:5000/api/1.0/post_qwa/11EC2020-3AEA-4069-A2DD-08002B30309D
        
        """
        result = {}
        header_q = table.get_item(key_post=hashValidation(key))
        
        if header_q._data.get('win_answers'):
            win_answers = hashKeyList(list(header_q._data['win_answers']))
            winanswers_a = table.batch_get(win_answers) 
            result ={
                     "question": marshal(item_to_dict(header_q._data),format_timeline)
                    ,"winanswers": marshal(items_to_list(winanswers_a),format_timeline)
                    }  
        else:
            result ={
                     "question": marshal(item_to_dict(header_q._data),format_timeline)
                    ,"winanswers": []
                    }  
        
        return result


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
        
            curl http://localhost:5000/api/1.0/allanswers -d 'hash_key=11EC2020-3AEA-4069-A2DD-08002B30309D' -X GET
        
        """
        
        args = self.reqparse.parse_args()
        hash_key = args.hash_key
        
        answers = table.query_2(key_post_original__eq=hash_key
                                     ,limit=3
                                     ,index='VerTodoPublic'
                                     ,reverse=True)
        #,exclusive_start_key=_exclusive_start_key

        return items_to_list(answers)


class Timeline_Update(Resource):
     
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hash_key', type=hashValidation, required=False)
        self.reqparse.add_argument('jsontimeline', type=str, required=False)
        self.reqparse.add_argument('plus', type=int, required=False)
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
                                      "message140": "Howto work with json in flask?"
                                    , "source": "web"
                                    , "geolocation": "4.598056,-74.075833"
                                    , "skills": ["flask","json","web"]
                                    , "link": "http://test1"
                                    , "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea"
                                }'
                 -X POST
             
            curl http://localhost:5000/api/1.0/post_a 
                -d 'jsontimeline=
                                {
                                      "message140": "see the video"
                                    , "source": "web"
                                    , "geolocation": "4.598056,-74.075833"
                                    , "link": "Imagen de Pregunta"
                                    , "key_user": "12345678-e9f0-69cc-1c68-362d8f5164ea"
                                    , "key_post_original" : "c20edb33-4dc7-43c7-bc8b-8ee3365a609b"
                                }' 
                -X POST
        
        """
        
        args = self.reqparse.parse_args()
        posting = jsondecoder(args.jsontimeline)
        
        posting['key_post'] = hashCreate()
        posting['key_timeline_post'] = timeUTCCreate()
        
        if not posting.get('key_post_original'):
            posting['flag_answer'] = 'False'
            posting['skills'] = set(posting['skills'])
            posting['total_answers'] = 0
        else:
            post_original = table.get_item(key_post=posting['key_post_original'])
            post_original._data['flag_answer'] = 'True'
            post_original._data['total_answers'] += 1
            post_original.save()
        
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
            "state" : int -> 1 add 0 remove
            ,"hash_key" : "str" -> UUID
            }    
        
        hash_key= 
            "str" -> UUID  
        
        Examples:
            
==============================================================================
            
        curl http://localhost:5000/api/1.0/update 
            -d 'hash_key=11EC2020-3AEA-4069-A2DD-08002B30309D' 
            -d 'jsontimeline={
                               "state" : 1
                              ,"hash_key_answer" : "41EC2020-3AEA-4069-A2DD-08002B30309D"
                              }' 
            -X PUT
            
        curl http://localhost:5000/api/1.0/update 
            -d 'hash_key=11EC2020-3AEA-4069-A2DD-08002B30309D' 
            -d 'jsontimeline={
                               "state" : 0
                              ,"hash_key_answer" : "41EC2020-3AEA-4069-A2DD-08002B30309D"
                              }' 
            -X PUT
        """
        args = self.reqparse.parse_args()
        
        item = table.get_item(key_post=args.hash_key)
        attributes = {}
        #item._data['flag_answer'] = 1
        
        if args.get('jsontimeline'):
            attributes = jsondecoder(args.jsontimeline)
        
        if not item._data.get('win_answers'):  
            item._data['win_answers'] = set([attributes["hash_key_answer"]])
            item.save()
            return 'Actualizado'    
            
        if attributes["state"]:
            item._data['win_answers'].add(attributes["hash_key_answer"])
        else:
            item._data['win_answers'].remove(attributes["hash_key_answer"])
        
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
            -d 'hash_key=41EC2020-3AEA-4069-A2DD-08002B30309D' 
            -X DELETE -v 
            
        """
        
        args = self.reqparse.parse_args()
        hash_key = args.hash_key
        questionItem = None
        message = {"success" : {
                                "message": "delete successful from timeline", 
                                "status": "Removed"
                                }
                    ,"error":{
                                "message": "delete fail from timeline", 
                                "status": "NoChange"
                             }
                    }
         
        
#        db_connection.delete_item('timeline', key={'key_post':hash_key})
        
        deleteItem = table.get_item(key_post=hash_key)
#         deleteItem.next().delete()
  
        #Eliminando una pregunta
        if deleteItem._data.get('key_post_original'):
            questionItem = table.get_item(key_post=deleteItem._data['key_post_original'])       
        elif not deleteItem._data['total_answers']:
            db_connection.delete_item('timeline', key={'key_post':hash_key})
            return message['success']
 
        else:
            return message['error']
         
        #Eliminando una respuesta
        if not questionItem._data.get('win_answers'): 
            questionItem._data['total_answers'] -= 1
            questionItem.save()
            db_connection.delete_item('timeline', key={'key_post':hash_key})
            return message['success']
 
        if not hash_key in questionItem._data['win_answers']:
            questionItem._data['total_answers'] -= 1
            questionItem.save()
            db_connection.delete_item('timeline', key={'key_post':hash_key})
            return message['success']

        return message['error']
        
        
    
    
    
