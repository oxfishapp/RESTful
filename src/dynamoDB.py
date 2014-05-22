from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import GlobalIncludeIndex, GlobalAllIndex, GlobalKeysOnlyIndex
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import STRING, NUMBER

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
        throughput={'read': 5, 'write': 3}
        
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
        
#         if table.delete(): 
#             tables['TableNames'].remove(table_name)
        
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
             HashKey('Key_Post',data_type = STRING),
             #RangeKey('Key_TimelinePost',data_type = STRING),
             ]
        
        throughput={'read': 5, 'write': 3}
        
        
        
        GAI_TimelinePublic = GlobalAllIndex('GAI_TimelinePublic'
                                               ,parts=[HashKey('FlagAnswer',data_type = NUMBER)
                                               ,RangeKey('Key_TimelinePost',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        GAI_VerTodoPublic = GlobalAllIndex('GAI_VerTodoPublic'
                                               ,parts=[HashKey('Key_PostOriginal',data_type = STRING),
                                                       RangeKey('Key_TimelinePost',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        GAI_Home = GlobalAllIndex('GAI_Home'
                                      ,parts=[HashKey('Key_User',data_type = STRING),
                                              RangeKey('Key_TimelinePost',data_type = STRING)
                                              ]
                                      ,throughput=throughput
                                       )
        
        table_name = 'timeline' + self.TABLE_SUFFIX
        
        table = Table(table_name, connection=self.db_connection)
        
#         if table.delete(): 
#             tables['TableNames'].remove(table_name)
        
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
                         )
        
        self.dynamodb.tables['tbl_timeline'] = table

    def super_create_table_skill(self):
                
        #Creacion de la tabla user_suffix_ (ej. user_tets_)
        tables = self.db_connection.list_tables()
        schema_table = [
             HashKey('Skill',data_type = STRING),
             RangeKey('Key_Time',data_type = STRING),
             ]
        
        throughput={'read': 5, 'write': 3}
        
        GKOI_Navbar = GlobalKeysOnlyIndex('GKOI_Navbar'
                                               ,parts=[HashKey('Key_User',data_type = STRING)
                                               ,RangeKey('Skill',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        GKOI_Count = GlobalKeysOnlyIndex('GKOI_Count'
                                               ,parts=[HashKey('Skill',data_type = STRING)
                                               ,RangeKey('Skill_User',data_type = STRING)
                                                       ]
                                               ,throughput=throughput
                                               )
        
        table_name = 'skill' + self.TABLE_SUFFIX
        
        table = Table(table_name, connection=self.db_connection)
            
#         if table.delete(): 
#             tables['TableNames'].remove(table_name)
          
        if table_name in tables['TableNames'] and table_name.endswith('_'):
            if table.delete(): 
                tables['TableNames'].remove(table_name)
        
     
        if not table_name in tables['TableNames']:
            Table.create(table_name
                         , schema=schema_table
                         , throughput=throughput
                         , global_indexes=[GKOI_Navbar,GKOI_Count]
                         , connection=self.db_connection
                         )
        
        self.dynamodb.tables['tbl_skill'] = table


class dbTablesTest(dbTables):
    
    def __init__(self, database):
        super(dbTablesTest, self).__init__(database)
        
    def create_tables(self):
        super(dbTablesTest, self).create_tables()
        table = self.dynamodb.tables['tbl_user']
         
        for i in range(5):
             
            item = Item(table
                        ,data={'key_twitter': str(i)
                               ,'key_user': '550e8400-e29b-41d4-a716-44000000000' + str(i)
                               ,'nickname': 'nickname_user_' + str(i)
                               ,'name' : 'name_user_' + str(i)
                               ,'registered': '2013-10-0' + str(i) +' 23:18:01'
                               ,'link_image': 'http://twitter.com/user_' + str(i) + '/image'
                               ,'total_post': i * 10
                               ,'score_answers': i * 5
                               }
                        )
            item.save()


class dbTablesDev(dbTables):
    
    def __init__(self, database):
        super(dbTablesDev, self).__init__(database)
        
    def create_tables(self):
        super(dbTablesDev, self).create_tables()
        self.create_table_user()
        self.create_table_timeline()
        self.create_table_skill()
        
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
            
    def create_table_timeline(self):
        table = self.dynamodb.tables['tbl_timeline']
#         #x = table.get_item(key_twitter = '85721956')
#         if False: #not x:
        count = table.query_count(Key_Post__eq = '11EC2020-3AEA-4069-A2DD-08002B30309D')
        if count == 0:
                item = Item(  table
                            , data={
                                    'Key_Post'          : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Key_TimelinePost' : '2014-05-13 17:24:31'
                                    ,'Geolocation'      : '4.598056,-74.075833'
                                    ,'TotalAnswers'     : 3
                                    ,'Tags'             : set(['Flask','Python','dynamoDB'])
                                    ,'Source'           : 'Web'
                                    ,'Message140'          : 'Howto Create a table with Python in dynamoDB from Flask?'
                                    ,'Key_User'         : 'AEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'FlagAnswer'       : 1
                                    ,'WinAnswers'       : set(['31EC2020-3AEA-4069-A2DD-08002B30309D'])
                                    ,'Link'             : 'Imagen de Pregunta'
                                    }
                            )
                item.save()
                
                item = Item(  table
                            , data={
                                    'Key_Post'          : '21EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Key_TimelinePost' : '2014-05-14 17:24:31'
                                    ,'Geolocation'      : '4.598056,-74.075833'
                                    ,'Source'           : 'Web'
                                    ,'Message140'       : 'UNO link del video mas respuesta del usuario'
                                    ,'Key_User'         : 'BEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Key_PostOriginal' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Link'             : 'link video'
                                    }
                            )
                item.save()
                
                item = Item(  table
                            , data={
                                    'Key_Post'          : '31EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Key_TimelinePost' : '2014-05-15 17:24:31'
                                    ,'Geolocation'      : '4.598056,-74.075833'
                                    ,'Source'           : 'Web'
                                    ,'Message140'          : 'DOS link del video mas respuesta del usuario'
                                    ,'Key_User'         : 'CEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Key_PostOriginal' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Link'             : 'link video'
                                    }
                            )
                item.save()
                
                item = Item(  table
                            , data={
                                    'Key_Post'          : '41EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Key_TimelinePost' : '2014-05-15 17:24:31'
                                    ,'Geolocation'      : '4.598056,-74.075833'
                                    ,'Source'           : 'Web'
                                    ,'Message140'          : 'TRES link del video mas respuesta del usuario'
                                    ,'Key_User'         : 'DEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Key_PostOriginal' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Link'             : 'link video'
                                    }
                            )
                item.save()
                
                item = Item(  table
                            , data={
                                    'Key_Post'          : '12EC2020-3AEA-4069-A2DD-08002B30309D'
                                    ,'Key_TimelinePost' : '2014-05-13 17:24:31'
                                    ,'Geolocation'      : '4.598056,-74.075833'
                                    ,'Tags'             : set(['Flask','Python','dynamoDB'])
                                    ,'Source'           : 'Web'
                                    ,'Message140'          : 'Howto preunta sin resolver?'
                                    ,'Key_User'         : 'FFFF8765-4069-4069-A2DD-08002B30309D'
                                    ,'FlagAnswer'       : 0
                                    }
                            )
                item.save()

    def create_table_skill(self):
        from datetime import datetime
        str(datetime.utcnow())

        table = self.dynamodb.tables['tbl_skill']
        count = table.query_count(Skill__eq = 'DynamoDB',Skill_User__eq = 'True',index='GKOI_Count')
        if count == 0:
                item = Item(  table
                            , data={      
                                    'Skill' : 'DynamoDB'
                                    ,'Key_Time' :  str(datetime.utcnow())
                                    ,'Key_Post' : 'B2EC2020-3AEA-4069-A2DD-08002B30309D'})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Skill' : 'Flask'
                                    ,'Key_Time' :  str(datetime.utcnow())
                                    ,'Key_Post' : 'B2EC2020-3AEA-4069-A2DD-08002B30309D'})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Skill' : 'Python'
                                    ,'Key_Time' :  str(datetime.utcnow())
                                    ,'Key_Post' : 'B2EC2020-3AEA-4069-A2DD-08002B30309D'})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Skill' : 'CSharp'
                                    ,'Key_Time' :  str(datetime.utcnow())
                                    ,'Key_Post' : 'A2EC2020-3AEA-4069-A2DD-08002B30309D'})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Skill' : 'HTML'
                                    ,'Key_Time' :  str(datetime.utcnow())
                                    ,'Key_Post' : 'A2EC2020-3AEA-4069-A2DD-08002B30309D'})
                item.save()
        
                item = Item(  table
                            , data={   
                                    'Skill' : 'JQuery'
                                    ,'Key_Time' :  str(datetime.utcnow())
                                    ,'Key_Post' : 'A2EC2020-3AEA-4069-A2DD-08002B30309D'})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Key_User' : 'AEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Skill' : 'Python'
                                    ,'Skill_User' : 'True'
                                    ,'Key_Time' :  str(datetime.utcnow())})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Key_User' : 'AEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Skill' : 'Flask'
                                    ,'Skill_User' : 'True'
                                    ,'Key_Time' :  str(datetime.utcnow())})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Key_User' : 'AEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Skill' : 'DynamoDB'
                                    ,'Skill_User' : 'True'
                                    ,'Key_Time' :  str(datetime.utcnow())})
                item.save()
        
                item = Item(  table
                            , data={    
                                    'Key_User' : 'BEAF8765-4069-4069-A2DD-08002B30309D'
                                    ,'Skill' : 'CSharp'
                                    ,'Skill_User' : 'True'
                                    ,'Key_Time' :  str(datetime.utcnow())})
                item.save()

config_db_env = {
    'dev': dbTablesDev,
    'test': dbTablesTest,
    'default': dbTables
}
