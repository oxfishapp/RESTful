'''
Created on May 12, 2014

@author: anroco
'''

from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import STRING
from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import GlobalIncludeIndex

class dbTables(object):
    
    dynamodb = None
    TABLE_SUFFIX = ''
    db_connection = None
    
    def __init__(self, database):
        self.dynamodb = database
        self.TABLE_SUFFIX = database.config.DB_TABLE_SUFFIX
        self.db_connection = database.db_connection
    
    def create_tables(self):
        
        #Creacion de la tabla user_suffix_ (ej. user_tets_)
        tables = self.db_connection.list_tables()
        schema_table = [HashKey('key_twitter', data_type = STRING)]
        throughput={'read': 5, 'write': 3}
        
        key_user_index= GlobalIncludeIndex('key_user_index'
                                       , parts=[HashKey('key_user', data_type = STRING)]
                                       , throughput=throughput
                                       , includes=['nickname', 'name', 'link_image'],
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
                         , global_indexes=[key_user_index]
                         , connection=self.db_connection
                         )
        
        self.dynamodb.tables['tbl_user'] = table
 

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
        table = self.dynamodb.tables['tbl_user']
        x = table.get_item(key_twitter = '85721956')
        if not x:
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
    'dev': dbTablesDev,
    'test': dbTablesTest,
    'default': dbTables
}