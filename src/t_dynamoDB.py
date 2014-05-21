from boto.dynamodb2.fields import GlobalIncludeIndex, GlobalAllIndex
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

#Imprimo la lsita de tablas que se encuentran en DynamoDB
print ("Before Creation:")
print (tables)

schema_list = [
     HashKey('Key_Post',data_type = STRING),
     #RangeKey('Key_TimelinePost',data_type = STRING),
 ]

throughput_dict = {'read': 5, 'write': 2}

#HashKey('secondKey',data_type = STRING)
#data_type si no se especifica por default queda STRING

GAI_TimelinePublic = GlobalAllIndex('GAI_TimelinePublic'
                                       ,parts=[HashKey('FlagAnswer',data_type = NUMBER)
                                       ,RangeKey('Key_TimelinePost',data_type = STRING)
                                               ]
                                       ,throughput=throughput_dict
                                       )

GAI_VerTodoPublic = GlobalAllIndex('GAI_VerTodoPublic'
                                       ,parts=[HashKey('Key_PostOriginal',data_type = STRING),
                                               RangeKey('Key_TimelinePost',data_type = STRING)
                                               ]
                                       ,throughput=throughput_dict
                                       )

GAI_Home = GlobalAllIndex('GAI_Home'
                              ,parts=[HashKey('Key_User',data_type = STRING),
                                      RangeKey('Key_TimelinePost',data_type = STRING)
                                      ]
                              ,throughput=throughput_dict
                               )

table_name = 'TimelineV14'

table = Table(table_name, connection=conn)

if table_name not in tables['TableNames']:
    Table.create(table_name
        , schema=schema_list
        , throughput=throughput_dict
        , global_indexes=[GAI_TimelinePublic,
                          GAI_VerTodoPublic,
                          GAI_Home,]
        , connection=conn
    )
    
    item = Item(  table
                , data={
                        'Key_Post'          : '11EC2020-3AEA-4069-A2DD-08002B30309D'
                        ,'Key_TimelinePost' : '2014-05-13 17:24:31'
                        ,'Geolocation'      : '4.598056,-74.075833'
                        ,'TotalAnswers'     : 3
                        ,'Tags'             : set(['Flask','Python','DynamoDB'])
                        ,'Source'           : 'Web'
                        ,'Message140'          : 'Howto Create a table with Python in DynamoDB from Flask?'
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
                        ,'Tags'             : set(['Flask','Python','DynamoDB'])
                        ,'Source'           : 'Web'
                        ,'Message140'          : 'Howto preunta sin resolver?'
                        ,'Key_User'         : 'FFFF8765-4069-4069-A2DD-08002B30309D'
                        ,'FlagAnswer'       : 0
                        }
                )
    item.save()
    
data = table.query_2(
        FlagAnswer__eq=0
        ,limit=20
        ,index='GAI_TimelinePublic'
        #,exclusive_start_key=_exclusive_start_key
        )

for item in data:
    print dict(item)
