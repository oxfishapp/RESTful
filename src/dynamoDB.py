from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import GlobalIncludeIndex, GlobalAllIndex, GlobalKeysOnlyIndex
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import STRING, NUMBER
from boto import dynamodb2

class dbTables(object):
    
    dynamodb = None
    TABLE_SUFFIX = ''
    db_connection = None
    
    def __init__(self, database):
        self.dynamodb = database
        self.TABLE_SUFFIX = database.config.DB_TABLE_SUFFIX
        self.db_connection = database.db_connection
        
    def create_tables(self):
        self.super_create_table_user()
        self.super_create_table_timeline()
        self.super_create_table_skill()
    
    def super_create_table_user(self):
        
        #Creacion de la tabla user_suffix_ (ej. user_tets_)
        tables = self.db_connection.list_tables()
        schema_table = [HashKey('key_twitter', data_type = STRING)]
        throughput={'read': 20, 'write': 20}
        
        key_user_index= GlobalIncludeIndex('key_user_index'
                                       , parts=[HashKey('key_user', data_type = STRING)]
                                       , throughput=throughput
                                       , includes=['nickname', 'name', 'link_image'],
                                       )
        
        nickname_user_index= GlobalIncludeIndex('nickname_user_index'
                                       , parts=[HashKey('nickname', data_type = STRING)]
                                       , throughput=throughput
                                       , includes=['key_user'],
                                       )
        
        table_name = 'user' + self.TABLE_SUFFIX
        
        table = Table(table_name, connection=self.db_connection)
        
        if table.delete(): 
            tables['TableNames'].remove(table_name)
        
        if table_name in tables['TableNames'] and table_name.endswith('_'):
            if table.delete(): 
                tables['TableNames'].remove(table_name)
        
     
        if not table_name in tables['TableNames']:
            Table.create(table_name
                         , schema=schema_table
                         , throughput=throughput
                         , global_indexes=[key_user_index, nickname_user_index]
                         , connection=self.db_connection
                         )
        
        self.dynamodb.tables['tbl_user'] = table

    def super_create_table_timeline(self):
        
        #Creacion de la tabla user_suffix_ (ej. user_tets_)
        tables = self.db_connection.list_tables()
        schema_table = [
             HashKey('key_post',data_type = STRING),
             #RangeKey('key_timelinePost',data_type = STRING),
             ]
        
        throughput={'read': 20, 'write': 20}
        
        
        
        GAI_TimelinePublic = GlobalAllIndex('TimelinePublic'
                                               ,parts=[HashKey('flag_answer',data_type = STRING)
                                               ,RangeKey('key_timeline_post',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        GAI_VerTodoPublic = GlobalAllIndex('VerTodoPublic'
                                               ,parts=[HashKey('key_post_original',data_type = STRING),
                                                       RangeKey('key_timeline_post',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        GAI_Home = GlobalAllIndex('Home'
                                      ,parts=[HashKey('key_user',data_type = STRING),
                                              RangeKey('key_timeline_post',data_type = STRING)
                                              ]
                                      ,throughput=throughput
                                       )
        
        table_name = 'timeline' + self.TABLE_SUFFIX
        
        table = Table(table_name, connection=self.db_connection)
        
        if table.delete(): 
            tables['TableNames'].remove(table_name)
        
        if table_name in tables['TableNames'] and table_name.endswith('_'):
            if table.delete(): 
                tables['TableNames'].remove(table_name)
        
     
        if not table_name in tables['TableNames']:
            Table.create(table_name
                         , schema=schema_table
                         , throughput=throughput
                        , global_indexes=[GAI_TimelinePublic,
                                          GAI_VerTodoPublic,
                                          GAI_Home,]
                         , connection=self.db_connection
#                          dynamodb2.connect_to_region('us-west-2',
#                                                                  aws_access_key_id='key',
#                                                                  aws_secret_access_key='key',
#                                                                  )
                         )
        
        self.dynamodb.tables['tbl_timeline'] = table

    def super_create_table_skill(self):
                
        #Creacion de la tabla user_suffix_ (ej. user_tets_)
        tables = self.db_connection.list_tables()
        schema_table = [
             HashKey('skill',data_type = STRING),
             RangeKey('key_time',data_type = STRING),
             ]
        
        throughput={'read': 5, 'write': 3}
        
        GKOI_Navbar = GlobalKeysOnlyIndex('GKOI_Navbar'
                                               ,parts=[HashKey('key_user',data_type = STRING)
                                               ,RangeKey('skill',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        GII_Find = GlobalIncludeIndex('GII_Find'
                                               ,parts=[HashKey('skill',data_type = STRING)
                                               ,RangeKey('key_time',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               , includes=['key_post']
                                               )
        
        table_name = 'skill' + self.TABLE_SUFFIX
        
        table = Table(table_name, connection=self.db_connection)
            
        if table.delete(): 
            tables['TableNames'].remove(table_name)
          
        if table_name in tables['TableNames'] and table_name.endswith('_'):
            if table.delete(): 
                tables['TableNames'].remove(table_name)
        
     
        if not table_name in tables['TableNames']:
            Table.create(table_name
                         , schema=schema_table
                         , throughput=throughput
                         , global_indexes=[GKOI_Navbar,GII_Find]
                         , connection=self.db_connection
                         )
        
        self.dynamodb.tables['tbl_skills'] = table


class dbTablesTest(dbTables):
    
    def __init__(self, database):
        super(dbTablesTest, self).__init__(database)
    
    def create_tables(self):    
        super(dbTablesTest, self).create_tables()
        self.create_table_user()
        self.create_table_timeline()
        self.create_table_skill()
        
    def create_table_user(self):
        table = self.dynamodb.tables['tbl_user']
         
        item = Item(table,data={'key_twitter':'85721956'
                                 ,'key_user': 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                                 ,'nickname': 'anroco'
                                 ,'name' : 'Andres Rodriguez'
                                 ,'registered': '2014-05-09 23:59:59'
                                 ,'link_image': 'http://twitter.com/anroco/image'
                                 ,'total_post': 2983
                                 ,'score_answers': 827377
                               }
                        )
        item.save()
        
        item = Item(table,data={'key_twitter':'12345678'
                                 ,'key_user': '12345678-e9f0-69cc-1c68-362d8f5164ea'
                                 ,'nickname': 'viejoemer'
                                 ,'name' : 'Emerson Perdomo'
                                 ,'registered': '2014-05-21 23:59:59'
                                 ,'link_image': 'http://twitter.com/viejoemer/image'
                                 ,'total_post': 12
                                 ,'score_answers': 12
                               }
                        )
        item.save()
        
        item = Item(table,data={'key_twitter':'87654321'
                                 ,'key_user': '87654321-e9f0-69cc-1c68-362d8f5164ea'
                                 ,'nickname': 'franper'
                                 ,'name' : 'Francisco Perez'
                                 ,'registered': '2014-05-22 23:59:59'
                                 ,'link_image': 'http://twitter.com/franper/image'
                                 ,'total_post': 2
                                 ,'score_answers': 1
                               }
                        )
        item.save()
        
    def create_table_timeline(self):
        table = self.dynamodb.tables['tbl_timeline']
        item = Item(  table
                    , data={
                            'key_post'          : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'key_timeline_post' : '2014-05-13 17:24:31'
                            ,'geolocation'      : '4.598056,-74.075833'
                            ,'total_answers'     : 3
                            ,'skills'             : set(['flask','python','dynamodb'])
                            ,'source'           : 'Web'
                            ,'message140'          : 'Howto Create a table with Python in dynamodb from Flask?'
                            ,'key_user'         : 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                            ,'flag_answer'       : 'True'
                            ,'win_answers'       : set(['31EC2020-3AEA-4069-A2DD-08002B30309D','21EC2020-3AEA-4069-A2DD-08002B30309D'])
                            ,'link'             : 'Imagen de Pregunta'
                            }
                    )
        item.save()
        
        item = Item(  table
                    , data={
                            'key_post'          : '21EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'key_timeline_post' : '2014-05-14 17:24:31'
                            ,'geolocation'      : '4.598056,-74.075833'
                            ,'source'           : 'Web'
                            ,'message140'       : 'UNO link del video mas respuesta del usuario'
                            ,'key_user'         : '12345678-e9f0-69cc-1c68-362d8f5164ea'
                            ,'key_post_original' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'link'             : 'link video'
                            }
                    )
        item.save()
        
        item = Item(  table
                    , data={
                            'key_post'          : '31EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'key_timeline_post' : '2014-05-15 17:24:31'
                            ,'geolocation'      : '4.598056,-74.075833'
                            ,'source'           : 'Web'
                            ,'message140'          : 'DOS link del video mas respuesta del usuario'
                            ,'key_user'         : '87654321-e9f0-69cc-1c68-362d8f5164ea'
                            ,'key_post_original' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'link'             : 'link video'
                            }
                    )
        item.save()
        
        item = Item(  table
                    , data={
                            'key_post'          : '41EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'key_timeline_post' : '2014-05-15 17:24:31'
                            ,'geolocation'      : '4.598056,-74.075833'
                            ,'source'           : 'Web'
                            ,'message140'          : 'TRES link del video mas respuesta del usuario'
                            ,'key_user'         : '87654321-e9f0-69cc-1c68-362d8f5164ea'
                            ,'key_post_original' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'link'             : 'link video'
                            }
                    )
        item.save()
        
        item = Item(  table
                    , data={
                            'key_post'          : '12EC2020-3AEA-4069-A2DD-08002B30309D'
                            ,'key_timeline_post' : '2014-05-13 17:24:31'
                            ,'geolocation'      : '4.598056,-74.075833'
                            ,'skills'             : set(['csharp','html','jquery'])
                            ,'source'           : 'Web'
                            ,'message140'          : 'Howto preunta sin resolver?'
                            ,'key_user'         : '87654321-e9f0-69cc-1c68-362d8f5164ea'
                            ,'flag_answer'       : 'False'
                            ,'total_answers' : 0
                            }
                    )
        item.save()

    def create_table_skill(self):
        from datetime import datetime

        table = self.dynamodb.tables['tbl_skills']
        
        #######################################################################################
        #######################################PREGUNTAS#######################################
        #######################################PREGUNTAS#######################################
        #######################################PREGUNTAS#######################################
        
        item = Item(  table
                    , data={      
                            'skill' : 'q_dynamodb'
                            ,'key_time' :  str(datetime.utcnow())
                            ,'key_post' : '11EC2020-3AEA-4069-A2DD-08002B30309D'})
        item.save()

        item = Item(  table
                    , data={    
                            'skill' : 'q_flask'
                            ,'key_time' :  str(datetime.utcnow())
                            ,'key_post' : '11EC2020-3AEA-4069-A2DD-08002B30309D'})
        item.save()

        item = Item(  table
                    , data={    
                            'skill' : 'q_python'
                            ,'key_time' :  str(datetime.utcnow())
                            ,'key_post' : '11EC2020-3AEA-4069-A2DD-08002B30309D'})
        item.save()

        item = Item(  table
                    , data={    
                            'skill' : 'q_csharp'
                            ,'key_time' :  str(datetime.utcnow())
                            ,'key_post' : '12EC2020-3AEA-4069-A2DD-08002B30309D'})
        item.save()

        item = Item(  table
                    , data={    
                            'skill' : 'q_dynamodb'
                            ,'key_time' :  str(datetime.utcnow())
                            ,'key_post' : '12EC2020-3AEA-4069-A2DD-08002B30309D'})
        item.save()

        item = Item(  table
                    , data={   
                            'skill' : 'q_jquery'
                            ,'key_time' :  str(datetime.utcnow())
                            ,'key_post' : '12EC2020-3AEA-4069-A2DD-08002B30309D'})
        item.save()

        ##################################################################################
        #######################################USER#######################################
        #######################################USER#######################################
        #######################################USER#######################################
        item = Item(  table
                    , data={    
                            'key_user' : 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'python'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()

        item = Item(  table
                    , data={    
                            'key_user' : 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'flask'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()

        item = Item(  table
                    , data={    
                            'key_user' : 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'dynamodb'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()

        item = Item(  table
                    , data={    
                            'key_user' : '12345678-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'csharp'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()
        
        item = Item(  table
                    , data={    
                            'key_user' : '12345678-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'dynamodb'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()

        item = Item(  table
                    , data={    
                            'key_user' : '87654321-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'flask'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()

        item = Item(  table
                    , data={    
                            'key_user' : '87654321-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'csharp'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()
        
        item = Item(  table
                    , data={    
                            'key_user' : '87654321-e9f0-69cc-1c68-362d8f5164ea'
                            ,'skill' : 'dynamodb'
                            ,'key_time' :  str(datetime.utcnow())})
        item.save()

class dbTablesDev(dbTables):
    
    def __init__(self, database):
        super(dbTablesDev, self).__init__(database)
        
    def create_tables(self):
        super(dbTablesDev, self).create_tables()
#         self.create_table_user()
#         self.create_table_timeline()
#         self.create_table_skill()
        
    def create_table_user(self):
        table = self.dynamodb.tables['tbl_user']
        item = table.query_count(key_twitter__eq = '85721956')
        if not item :
            item = Item(table ,data={'key_twitter':'85721956'
                                     ,'key_user': 'fedcf7af-e9f0-69cc-1c68-362d8f5164ea'
                                     ,'nickname': 'anroco'
                                     ,'name' : 'Andres Rodriguez'
                                     ,'registered': '2014-05-09 23:59:59'
                                     ,'link_image': 'http://twitter.com/anroco/image'
                                     ,'total_post': 2983
                                     ,'score_answers': 827377
                                   }
                            )
            item.save()
            


config_db_env = {
    'dev': dbTablesTest,
    'test': dbTablesTest,
    'default': dbTables
}
