from application import dynamodb
from commons import *
from boto.dynamodb2.items import Item
'''
Created on May 25, 2014

@author: root
'''

db_connection = dynamodb.db_connection
table_skill = dynamodb.tables['tbl_skills']
table_user = dynamodb.tables['tbl_user']
table_timeline = dynamodb.tables['tbl_timeline']

PREFIX = 'q_'
LIMIT = 10

class Skill():

    #Crea todos los skills de un usuario en la tabla skill
    def put_skills_user(self, skills, key_user,):
        self._put_skills(skills, key_user, '')
    
    #Crea todos los skills de un post en la tabla skill
    def put_skills_post(self, skills, key_post):
        self._put_skills(skills, key_post, PREFIX)
        
    #Funcion de apoyo, inserta skills en la tabla skill    
    def _put_skills(self, skills, key, prefix):
        for skill in skills:
            self._put_skill(skill, key, prefix)
    
    #Funcion de apoyo, inserta un skill en la tabla skill
    def _put_skill(self, skill, key_user, prefix):
        table_skill.put_item(data={'key_user' : key_user
                            ,'skill' : prefix + skill
                            ,'key_time' :  timeUTCCreate()}
                             )
    
    #Retorna los skills de un post en particular
    def skills_from_post(self, hash_key):
        return db_connection.query('skill', { 
                                            "key_post": 
                                                      { 
                                              "ComparisonOperator": "EQ",
                                              "AttributeValueList": [ {"S": hash_key} ]
                                                      }
                                                   }, index_name='GII_Post')
    #http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html#ConditionalExpressions
    #Elimina todo los skills asociados a un post
    def delete_skills_from_post(self, hash_key):
        values = self.skills_from_post(hash_key)
        for skill in dict(values.items())['Items']:
            db_connection.delete_item('skill', key={'skill':PREFIX + skill['key_time']['S']
                                                    ,'key_time':skill['key_time']['S']
                                                    })
    
    #Retorna un timeline de un skill en particular
    def finder(self, skill):
        return table_skill.query_2(skill__eq= PREFIX + skill
                                  , reverse=True
                                  , limit=LIMIT
                                  , index='GII_Find')
        
    #Retorna en total de usuarios que tienen un skill en particular    
    def count(self,skill):
        return table_skill.query_count(skill__eq=skill)

  
class Timeline():

    #Elimina una pregunta en particular con las habilidades asociadas
    def delete_question(self, key):
        self._delete_post(key)
        cskill = Skill()
        cskill.delete_skills_from_post(key)
        return 'TLQWA'
    
    #Elimina una respuesta de una pregunta
    def delete_answer(self, key, answer):
        question = self.get_post(answer._data['key_post_original'])
        if question._data.get('win_answers'): 
            if not key in question._data['win_answers']:
                return self._delete_post_answer(key_delete=key,question_update = question)
        else:
            return self._delete_post_answer(key_delete=key,question_update = question)
        
        return None
    
    #Funcion de apoyo elimina una respuesta y reduce en 1 
    #el total de respuestas de una pregunta
    def _delete_post_answer(self, key_delete, question_update):
        self._delete_post(key_delete)
        self._minus_one_total_answers(data=question_update)
        return 'TLA'        
        
    #Funcion de apoyo, elimina un post    
    def _delete_post(self,key):   
        db_connection.delete_item('timeline', key={'key_post':key})
         
    #Retorna un item de la tabla timeline        
    def get_post(self,key):
        return table_timeline.get_item(key_post=hashValidation(key))
    
    #Retorna una serie de items de la tabla timeline
    def get_posts(self,keys):
        return table_timeline.batch_get(keys) 

    #Devuelve una serie de items que crean el timeline public
    def public(self):
        return table_timeline.query_2(flag_answer__eq='True'
                                       ,limit=LIMIT
                                       ,index='TimelinePublic'
                                       ,reverse=True)
        
    #Devuelve una serie de items que crean el home de un usuario   
    def home(self,key):
        return table_timeline.query_2(key_user__eq=key
                                      ,limit=LIMIT
                                      ,index='Home'
                                      ,reverse=True)
    
    #Devuelve una serie de items que crean el timeline de una pregunta en particular    
    def answers(self,hash_key):
        return table_timeline.query_2(key_post_original__eq=hash_key
                                     ,limit=LIMIT
                                     ,index='VerTodoPublic'
                                     ,reverse=True)
        
    #Funcion de apoyo, Suma +1 al total de respuesta de una pregunta    
    def _plus_one_total_answers(self, key=None, data=None):
        if not data:
            data = self.get_post(key)
        data._data['flag_answer'] = 'True'
        self._minus_plus(data,1)

    #Funcion de apoyo, resta -1 al total de respuesta de una pregunta     
    def _minus_one_total_answers(self, key=None, data=None):   
        if not data:
            data = self.get_post(key)
        self._minus_plus(data, -1)   

    #Funcion de apoyo, Suma +1 o resta -1 al total de respuesta de una pregunta 
    def _minus_plus(self,data,number):
        data._data['total_answers'] += number
        data.save()
        
    #Crea una respuesta en la tabla timeline
    def create_post_answer(self,data): 
        self._plus_one_total_answers(key=data['key_post_original'])
        self._create_post(data)  

    #Crea un post en la tabla timeline
    def create_post_question(self,data):
        data['flag_answer'] = 'False'
        data['skills'] = set(data['skills'])
        data['total_answers'] = 0
        self._create_post(data)       

    #Funcion de apoyo para crear items en la tabla timeline
    def _create_post(self,data):
        data['key_post'] = hashCreate()
        data['key_timeline_post'] = timeUTCCreate()
        post = Item(table_timeline, data)
        post.save()
        
class User():
    pass











