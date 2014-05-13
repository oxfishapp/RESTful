import uuid
from boto.dynamodb2.fields import GlobalIncludeIndex
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection #DynamoDB Conexion
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import STRING, NUMBER

#Conexion
conn = DynamoDBConnection(
    host='localhost',
    port=8000,
    aws_access_key_id='DEVDB', #anything will do
    aws_secret_access_key='DEVDB', #anything will do
    is_secure=False)

#Lista de tablas en DynamoDB
tables = conn.list_tables()

#Imprimo la lsita de tablas que se encuentran en DydamoDB
print ("Before Creation:")
print (tables)

schema_list = [
     HashKey('Key_Post',data_type = STRING),
     RangeKey('Key_TimelinePost',data_type = STRING),
 ]

throughput_dict = {'read': 5, 'write': 2}

#HashKey('secondKey',data_type = STRING)
#data_type si no se especifica por default queda STRING

GII_TimelinePublic = GlobalIncludeIndex('GII_Timeline_Public'
                                       ,parts=[HashKey('FlagAnswer',data_type = NUMBER)
                                       ,RangeKey('Key_TimelinePost',data_type = STRING)
                                               ]
                                       ,throughput=throughput_dict
                                       ,includes=['Geolocation'
                                                 ,'Message'
                                                 ,'TotalAnswers'
                                                 ,'Tags'
                                                 ,'Key_Post'
                                                 ,'Key_User'
                                                 ]
                                       )

GII_VerTodoPublic = GlobalIncludeIndex('GII_VerTodoPublic'
                                       ,parts=[HashKey('Key_PostOriginal',data_type = STRING),
                                               RangeKey('Key_TimelinePost',data_type = STRING)
                                               ]
                                       ,throughput=throughput_dict
                                       ,includes=['Geolocation'
                                                 ,'Message'
                                                 ,'TotalAnswers'
                                                 ,'Tags'
                                                 ,'Key_Post'
                                                 ,'Key_User'
                                                 ]
                                       )

GII_Home = GlobalIncludeIndex('GII_Home'
                              ,parts=[HashKey('Key_User',data_type = STRING),
                                      RangeKey('Key_TimelinePost',data_type = STRING)
                                      ]
                              ,throughput=throughput_dict
                              ,includes=['Geolocation'
                                         ,'Message'
                                         ,'TotalAnswers'
                                         ,'Tags'
                                         ,'Key_Post'
                                         ]
                               )

table_name = 'TimelineV2'

table = Table(table_name, connection=conn)

if table_name not in tables['TableNames']:
    Table.create(table_name
        , schema=schema_list
        , throughput=throughput_dict
        , global_indexes=[GII_TimelinePublic,
                          GII_VerTodoPublic,
                          GII_Home,]
        , connection=conn
    )
    
    item = Item(  table
                , data={
                        'Key_Post'          : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                        ,'Key_TimelinePost' : '2014-05-13 17:24:31'
                        ,'Geolocation'      : '4.598056,-74.075833'
                        ,'TotalAnswers'     : 2
                        ,'Language'         : 'en'
                        ,'Tags'             : set(['Flask','Python','DynamoDB'])
                        ,'Source'           : 'Web'
                        ,'Message'          : 'Howto Create a table with Python in DynamoDB from Flask?'
                        ,'Key_User'         : 'AEA-4069-A2DD-08002B30309D'
                        ,'FlagAnswer'       : 1
                        }
                )
    item.save()
    
    item = Item(  table
                , data={
                        'Key_Post'          : '21EC2020-3AEA-4069-A2DD-08002B30309D'
                        ,'Key_TimelinePost' : '2014-05-14 17:24:31'
                        ,'Geolocation'      : '4.598056,-74.075833'
                        ,'Language'         : 'es'
                        ,'Source'           : 'Web'
                        ,'Message'          : 'UNO link del video mas respuesta del usuario'
                        ,'Key_User'         : 'BEA-4069-A2DD-08002B30309D'
                        ,'Key_PostOriginal' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                        }
                )
    item.save()
    
    item = Item(  table
                , data={
                        'Key_Post'          : '31EC2020-3AEA-4069-A2DD-08002B30309D'
                        ,'Key_TimelinePost' : '2014-05-15 17:24:31'
                        ,'Geolocation'      : '4.598056,-74.075833'
                        ,'Language'         : 'es'
                        ,'Source'           : 'Web'
                        ,'Message'          : 'DOS link del video mas respuesta del usuario'
                        ,'Key_User'         : 'CEA-4069-A2DD-08002B30309D'
                        ,'Key_PostOriginal' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                        }
                )
    item.save()
    
    item = Item(  table
                , data={
                        'Key_Post'          : '12EC2020-3AEA-4069-A2DD-08002B30309D'
                        ,'Key_TimelinePost' : '2014-05-13 17:24:31'
                        ,'Geolocation'      : '4.598056,-74.075833'
                        ,'Language'         : 'en'
                        ,'Tags'             : set(['Flask','Python','DynamoDB'])
                        ,'Source'           : 'Web'
                        ,'Message'          : 'Howto preunta sin resolver?'
                        ,'Key_User'         : 'TTT-4069-A2DD-08002B30309D'
                        ,'FlagAnswer'       : 0
                        }
                )
    item.save()
