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

    def post_skills_user(self, skills, key_user,):
        '''(list, UUID) -> NoneType
        
        Crea todos los skills de un usuario en la tabla skill.
        
        
        '''
        self._post_skills(skills, key_user, '')
    
    def post_skills_post(self, skills, key_post):
        '''(list, UUID) -> NoneType
        
        Crea todos los skills de un post en la tabla skill.
        
        '''
        self._post_skills(skills, key_post, PREFIX)
          
    def _post_skills(self, skills, key, prefix):
        '''(list, UUID, str) -> NoneType
        
        Funcion de apoyo, inserta skills en la tabla skill.
        
        '''
        for skill in skills:
            self._post_skill(skill, key, prefix)
    
    def _post_skill(self, skill, key_user, prefix):
        '''(list, UUID, str) -> NoneType
        
        Funcion de apoyo, inserta un skill en la tabla skill.
        
        '''
        table_skill.put_item(data={'key_user' : key_user
                            ,'skill' : prefix + skill
                            ,'key_time' :  timeUTCCreate()}
                             )
    
    def skills_from_post(self, hash_key):
        '''(UUID) -> Resultset
        
        Retorna los skills de un post en particular.
        
        '''
        return db_connection.query('skill', { 
                                            "key_post": 
                                                      { 
                                              "ComparisonOperator": "EQ",
                                              "AttributeValueList": [ {"S": hash_key} ]
                                                      }
                                                   }, index_name='GII_Post')
    #http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html
    #http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/MonitoringDynamoDB.html
    
    def delete_skills_from_post(self, hash_key):
        '''(UUID) -> NoneType
        
        Elimina todos los skills asociados a un post.
        
        '''
        
        values = self.skills_from_post(hash_key)
        for skill in dict(values.items())['Items']:
            db_connection.delete_item('skill', key={'skill':PREFIX + skill['key_time']['S']
                                                    ,'key_time':skill['key_time']['S']
                                                    })
    
    def finder(self, skill):
        '''(str) -> Resultset
        
        Retorna la linea de tiempo de un skill en particular.
        
        '''
        
        return table_skill.query_2(skill__eq= PREFIX + skill
                                  , reverse=True
                                  , limit=LIMIT
                                  , index='GII_Find')
          
    def count(self,skill):
        '''(str)
        
        Retorna el total de usuarios que tienen un skill en particular.
        
        '''
        return table_skill.query_count(skill__eq=skill)

  
class Timeline():

    def delete_question(self, key):
        '''(UUID) -> status
        
        Eliminar una pregunta en particular con las habilidades asociadas.
        
        '''
        self._delete_post(key)
        cskill = Skill()
        cskill.delete_skills_from_post(key)
        return 'TLQWA'
    
    def delete_answer(self, key, answer):
        '''(UUID,item) -> status
        
        Elimina una respuesta asociada a una pregunta.
        
        '''
        question = self.get_post(answer._data['key_post_original'])
        if question._data.get('win_answers'): 
            if not key in question._data['win_answers']:
                return self._delete_post_answer(key_delete=key,question_update = question)
        else:
            return self._delete_post_answer(key_delete=key,question_update = question)
        
        return None
    
    def _delete_post_answer(self, key_delete, question_update):
        '''(UUID,item) -> status
        
        Funcion de apoyo, alimina una respuesta y reduce en 1
        el total de respuesta de una pregunta.
        
        '''
        self._delete_post(key_delete)
        self._minus_one_total_answers(data=question_update)
        return 'TLA'        
        
    def _delete_post(self,key):   
        '''(UUID) -> NoneType
        
        Funcion de apoyo, elimina un post.
        
        '''
        db_connection.delete_item('timeline', key={'key_post':key})
             
    def get_post(self,key):
        '''(UUID) -> item
        
        Retorna un item de la tabla timeline.
        
        '''
        return table_timeline.get_item(key_post=hashValidation(key))
    
    def get_posts(self,keys):
        '''(list) -> Resultset
        
        Retorna una serie de items de la tabla timeline.
        
        '''
        return table_timeline.batch_get(keys) 

    def public(self):
        '''() -> Resultset
        
        Devuelve una serie de items que crean el timeline public.
        
        '''
        return table_timeline.query_2(flag_answer__eq='True'
                                       ,limit=LIMIT
                                       ,index='TimelinePublic'
                                       ,reverse=True)
        
    def home(self,key):
        '''(UUID) -> Resultset
        
        Devuelve una serie de items que crean el home de un usuario.
        
        '''
        return table_timeline.query_2(key_user__eq=key
                                      ,limit=LIMIT
                                      ,index='Home'
                                      ,reverse=True)
    
    def answers(self,hash_key):
        '''(UUID) -> Resultset
        
        Devuelve una serie de items que crean el timeline de una
        pregunta en particular.
        
        '''
        return table_timeline.query_2(key_post_original__eq=hash_key
                                     ,limit=LIMIT
                                     ,index='VerTodoPublic'
                                     ,reverse=True)
          
    def _plus_one_total_answers(self, key=None, data=None):
        '''(UUID,item) -> NoneType
        
        Funcion de apoyo, suma 1 al total de respuestas de una pregunta
        
        '''
        if not data:
            data = self.get_post(key)
        data._data['flag_answer'] = 'True'
        self._minus_plus(data,1)

    def _minus_one_total_answers(self, key=None, data=None):   
        '''(UUID,item) -> NoneType
        
        Funcion de apoyo, resta 1 al total de respuestas de una pregunta.
        
        '''
        if not data:
            data = self.get_post(key)
        self._minus_plus(data, -1)   

    def _minus_plus(self,data,number):
        '''(item,int) -> NoneType
        
        Funcion de apoyo, suma 1 o resta 1 al total de respuestas de una pregunta.
        
        '''
        data._data['total_answers'] += number
        data.save()
        
    def create_post_answer(self,data): 
        '''(dict) -> None
        
        Crea una respuesta en la tabla timeline
        
        '''
        self._plus_one_total_answers(key=data['key_post_original'])
        self._create_post(data)  

    def create_post_question(self,data):
        '''(dict) -> NoneType
        
        Crea un post en la tabla timeline
        
        '''
        data['flag_answer'] = 'False'
        data['skills'] = set(data['skills'])
        data['total_answers'] = 0
        self._create_post(data)       

    def _create_post(self,data):
        '''(item) -> NoneType
        
        Funcion de apoyo, crea un item en la tabla timeline
        
        '''
        data['key_post'] = hashCreate()
        data['key_timeline_post'] = timeUTCCreate()
        post = Item(table_timeline, data)
        post.save()
        
class User():
    pass











