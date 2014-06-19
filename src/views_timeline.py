# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask.ext.restful import Resource, reqparse, marshal_with, marshal
from views_formats import format_timeline
from commons import item_to_dict, items_to_list, hashKeyList, hashValidation ,jsondecoder, pagination
from dynamoDBqueries import Timeline
from flask import abort

ctimeline = Timeline()

class HW(Resource):
    def get(self):   
        return 'Hellow World!'

#Global All Index Timeline Public
class Timeline_Index(Resource):
    #decorators = [marshal_with(format_timeline)]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pagination', type=str, required=True)
        #super(Timeline_Answers, self).__init__()  
    
    def get(self):
        ''' () -> list
        
        Retorna la lista de preguntas en la vista
        Publica de Oxfish.  
        
        Example:
            curl http://localhost:5000/api/1.0/publictimeline
            
        Result:
            [
                {
                    "flag_answer": "True", 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-13 17:24:31", 
                    "key_user": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "11EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": null
                    }, 
                    "link": "Imagen de Pregunta", 
                    "link_image": "http://twitter.com/anroco/image", 
                    "message140": "Howto Create a table with Python in dynamodb from Flask?", 
                    "name": "Andres Rodriguez", 
                    "nickname": "anroco", 
                    "skills": [
                        "flask", 
                        "python", 
                        "dynamodb"
                    ], 
                    "source": "Web", 
                    "total_answers": 3, 
                    "win_answers": [
                        "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "21EC2020-3AEA-4069-A2DD-08002B30309D"
                    ]
                }
            ]
             
        '''
        
        args = self.reqparse.parse_args()
        exclusive_start_key = jsondecoder(args.pagination)
        
        result = ctimeline.public(_exclusive_start_key=exclusive_start_key)
        
        data = items_to_list(result)
        
        #################################
        #__valor = result._last_key_seen
        ################################
        #Format = dict: {u'flag_answer': u'True', u'key_timeline_post': u'2014-06-19 20:44:59.370969', u'key_post': u'9c13be98-a9af-4a53-9e70-03a3bf1ddd67'}           
        
        data_format = marshal(data,format_timeline)
        
#         if not result._last_key_seen:
#             data_format.append(not result._last_key_seen)
#         else:
#             data_format.append(None)
               
        return pagination(data_format,result._last_key_seen)
    
#Global All Index Home
class Timeline_Home_Index(Resource):
    
    #decorators = [marshal_with(format_timeline)]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pagination', type=str, required=True)
        #super(Timeline_Answers, self).__init__()  
    
    def get(self, key):
        ''' (str) -> list
        
        Retorna una lista con las publicaciones realizadas
        por un usuario en particular.   
        
        Formato con el cual consulta en la tabla timeline
        para obtener el Home de un usuario en particular:
        
        key= 
            "str" -> UUID  
            
        Example:
            curl http://localhost:5000/api/1.0/home/87654321-e9f0-69cc-1c68-362d8f5164ea
        
        Result:
            [
                {
                    "flag_answer": null, 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-15 17:24:31", 
                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                    }, 
                    "link": "link video", 
                    "link_image": "http://twitter.com/franper/image", 
                    "message140": "DOS link del video mas respuesta del usuario", 
                    "name": "Francisco Perez", 
                    "nickname": "franper", 
                    "skills": null, 
                    "source": "Web", 
                    "total_answers": 0, 
                    "win_answers": null
                }, 
                {
                    "flag_answer": null, 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-15 17:24:31", 
                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "41EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                    }, 
                    "link": "link video", 
                    "link_image": "http://twitter.com/franper/image", 
                    "message140": "TRES link del video mas respuesta del usuario", 
                    "name": "Francisco Perez", 
                    "nickname": "franper", 
                    "skills": null, 
                    "source": "Web", 
                    "total_answers": 0, 
                    "win_answers": null
                },
                .
                .
                .
            ]
        
        '''
        vkey = hashValidation(key) 
        args = self.reqparse.parse_args()
        exclusive_start_key = jsondecoder(args.pagination)
        
        result = ctimeline.home(vkey,_exclusive_start_key=exclusive_start_key)
    
        data = items_to_list(result)
        
        #################################
        #__valor = result._last_key_seen
        ################################
        #Format = dict: {u'key_user': u'db5ae20f-3fd5-483f-9d8b-5e23169596a4', u'key_timeline_post': u'2014-06-19 20:48:41.659719', u'key_post': u'ea35cfd0-dccb-4816-8306-17e05222ad46'}
        
        data_format = marshal(data,format_timeline)
               
        return pagination(data_format,result._last_key_seen)


class Timeline_QandWinA(Resource):
    
    def get(self, key):
        ''' (str) -> dict
        
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
        
        Result:
            {
                "question": {
                    "flag_answer": "True", 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-13 17:24:31", 
                    "key_user": "fedcf7af-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "11EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": null
                    }, 
                    "link": "Imagen de Pregunta", 
                    "link_image": "http://twitter.com/anroco/image", 
                    "message140": "Howto Create a table with Python in dynamodb from Flask?", 
                    "name": "Andres Rodriguez", 
                    "nickname": "anroco", 
                    "skills": [
                        "flask", 
                        "python", 
                        "dynamodb"
                    ], 
                    "source": "Web", 
                    "total_answers": 3, 
                    "win_answers": [
                        "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "21EC2020-3AEA-4069-A2DD-08002B30309D"
                    ]
                }, 
                "winanswers": [
                    {
                        "flag_answer": null, 
                        "geolocation": "4.598056,-74.075833", 
                        "key_timeline_post": "2014-05-15 17:24:31", 
                        "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                        "keys": {
                            "hash_key": "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                            "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                        }, 
                        "link": "link video", 
                        "link_image": "http://twitter.com/franper/image", 
                        "message140": "DOS link del video mas respuesta del usuario", 
                        "name": "Francisco Perez", 
                        "nickname": "franper", 
                        "skills": null, 
                        "source": "Web", 
                        "total_answers": 0, 
                        "win_answers": null
                    }, 
                    .
                    .
                    .
            }
        
        '''
        result = {}
        vkey = hashValidation(key)
        header_q = ctimeline.get_post(vkey)
        
        if header_q._data.get('win_answers'):
            win_answers = hashKeyList(list(header_q._data['win_answers']))
            winanswers_a = ctimeline.get_posts(win_answers) 
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
    #decorators = [marshal_with(format_timeline)]  
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hash_key', type=hashValidation, required=True)
        self.reqparse.add_argument('pagination', type=str, required=True)
        #super(Timeline_Answers, self).__init__()  

    def get(self):
        ''' (str) -> list
        
        Retorna una lista cronológica con las respuestas
        de una pregunta en particular para ser cargadas 
        en la vista aloneview.
        
        Formato con el cual consulta en la tabla timeline
        para obtener la lista de respuestas de una pregunta:
        
        hash_key= 
            "str" -> UUID  
        
        Example:
        
            curl http://localhost:5000/api/1.0/allanswers 
                -d 'hash_key=11EC2020-3AEA-4069-A2DD-08002B30309D' 
                -X GET
                
        Result:
            [
                {
                    "flag_answer": null, 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-15 17:24:31", 
                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "31EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                    }, 
                    "link": "link video", 
                    "link_image": "http://twitter.com/franper/image", 
                    "message140": "DOS link del video mas respuesta del usuario", 
                    "name": "Francisco Perez", 
                    "nickname": "franper", 
                    "skills": null, 
                    "source": "Web", 
                    "total_answers": 0, 
                    "win_answers": null
                }, 
                {
                    "flag_answer": null, 
                    "geolocation": "4.598056,-74.075833", 
                    "key_timeline_post": "2014-05-15 17:24:31", 
                    "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea", 
                    "keys": {
                        "hash_key": "41EC2020-3AEA-4069-A2DD-08002B30309D", 
                        "hash_key_original": "11EC2020-3AEA-4069-A2DD-08002B30309D"
                    }, 
                    "link": "link video", 
                    "link_image": "http://twitter.com/franper/image", 
                    "message140": "TRES link del video mas respuesta del usuario", 
                    "name": "Francisco Perez", 
                    "nickname": "franper", 
                    "skills": null, 
                    "source": "Web", 
                    "total_answers": 0, 
                    "win_answers": null
                }, 
                .
                .
                .
            ]
        
        '''
        
        args = self.reqparse.parse_args()
        hash_key = args.hash_key
        exclusive_start_key = jsondecoder(args.pagination)
        
        result = ctimeline.answers(hash_key, _exclusive_start_key=exclusive_start_key) 
    
        data = items_to_list(result)
        
        #################################
        #__valor = result._last_key_seen
        ################################
        #Format = dict: {u'key_timeline_post': u'2014-06-19 20:48:24.385180', u'key_post_original': u'4a825921-78ef-44bb-bda0-0dd97789cfea', u'key_post': u'2c6c04ef-202d-4201-a836-777421686830'}
        
        data_format = marshal(data,format_timeline)
               
        return pagination(data_format,result._last_key_seen)


class Timeline_Update(Resource):
    
    #from api_errors import error_handled
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hash_key', type=hashValidation, required=False)
        self.reqparse.add_argument('key_user', type=hashValidation, required=False)
        self.reqparse.add_argument('jsontimeline', type=str, required=False)
        #super(Timeline_Update, self).__init__()   
    
    @marshal_with(format_timeline)
    def post(self):
        ''' () -> list
         
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
                    , "link": str
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
                                    , "link": "http://test1/Pregunta"
                                    , "key_user": "87654321-e9f0-69cc-1c68-362d8f5164ea"
                                }'
                 -X POST
             
            curl http://localhost:5000/api/1.0/post_a 
                -d 'jsontimeline=
                                {
                                      "message140": "see the video"
                                    , "source": "web"
                                    , "geolocation": "4.598056,-74.075833"
                                    , "link": "http://test2/Respuesta"
                                    , "key_user": "12345678-e9f0-69cc-1c68-362d8f5164ea"
                                    , "key_post_original" : "c20edb33-4dc7-43c7-bc8b-8ee3365a609b"
                                }' 
                -X POST
        
        '''
        
        args = self.reqparse.parse_args()
        posting = jsondecoder(args.jsontimeline)
        
        if not posting.get('key_user'):
            abort(400)
        
        if not posting.get('key_post_original'):
            ctimeline.create_post_question(posting)
        else:
            ctimeline.create_post_answer(posting)
        
        return items_to_list(posting)

    @marshal_with(format_timeline)
    def put(self):
        ''' () -> list
          
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
        '''
        args = self.reqparse.parse_args()
         
        item = ctimeline.get_post(args.hash_key)
        attributes = dict()
        
        if args.get('jsontimeline'):
            attributes = jsondecoder(args.jsontimeline)
            ctimeline.winanswers(item, attributes['hash_key_answer'], attributes['state'])
        
        return item._data
    
    @marshal_with(format_timeline)
    def delete(self):
        ''' () -> list
          
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
            
        key_user=
            "str" -> UUID  
             
        Examples:
         
        curl http://localhost:5000/api/1.0/delete 
            -d 'key_user=...'
            -d 'hash_key=41EC2020-3AEA-4069-A2DD-08002B30309D' 
            -X DELETE
             
        '''
        args = self.reqparse.parse_args()
        hash_key = args.hash_key
        
        deleteItem = ctimeline.get_post(hash_key)
        
        if args.key_user == deleteItem._data['key_user']:
            if deleteItem._data.get('key_post_original'):
                ctimeline.delete_answer(key=hash_key,answer=deleteItem)
            elif not deleteItem._data.get('total_answers'):
                ctimeline.delete_question(key=hash_key)
                
            return deleteItem._data
        
        abort(400)
