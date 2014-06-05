from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import (GlobalIncludeIndex, GlobalAllIndex,
                                   GlobalKeysOnlyIndex)
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import STRING


class dbTablesAWS(object):

    def __init__(self, database, config):
        '''
        (boto.dynamodb2.layer1.DynamoDBConnection) -> None

        Inicializa el objeto dbTables el cual permitira realizar el proceso
        de creacion de las tablas de la aplicacion.
        '''

        self.dynamodb = database
        self.db_connection = database.db_connection
        self.dynamodb.tables['tbl_user'] = Table(table_name=config['user'],
               connection=self.db_connection)
        self.dynamodb.tables['tbl_timeline'] = Table(table_name=config['timeline'],
               connection=self.db_connection)
        self.dynamodb.tables['tbl_skills'] = Table(table_name=config['skills'],
               connection=self.db_connection)


class dbTables(object):

    cnn = None
    tables = dict()
    config = None

    def __init__(self, config):
        '''
        (boto.dynamodb2.layer1.DynamoDBConnection) -> None

        Inicializa el objeto dbTables el cual permitira realizar el proceso
        de creacion de las tablas de la aplicacion.
        '''

        self.config = config
        self.create_connection()
        self.TABLE_PREFIX = config['DB_TABLE_PREFIX']

    def create_connection(self):
        from boto.dynamodb2.layer1 import DynamoDBConnection
        import dynamoDBqueries

        if dynamoDBqueries.db_connection is None:
            dynamoDBqueries.db_connection = DynamoDBConnection(host=self.config['DB_HOST'],
                        port=self.config['DB_PORT'],
                        aws_access_key_id=self.config['DB_AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=self.config['DB_AWS_SECRET_KEY'],
                        is_secure=self.config['DB_IS_SECURE'])
        self.cnn = dynamoDBqueries.db_connection

    def create_tables(self):
        '''
        () -> None

        Permite crear todas las tablas necesarias para el funcionamiento de la
        aplicacion.
        '''

        self.super_create_table_user()
        self.super_create_table_timeline()
        self.super_create_table_skill()

    def create_table(self, table_name, schema, throughput=None, indexes=None,
                     global_indexes=None):
        '''
        (str, list, dict, list, list) -> boto.dynamodb2.table.Table

        table_name: str con el nombre de la tabla a crear.
        schema: list de "BaseSchemaField" que representa el esquema de la tabla
        throughput: dict con 'read' & 'write' key y values enteros.
        indexes: list de "BaseIndexField" que define los indices de la tabla.
        global_indexes: list de "GlobalBaseIndexField" que define los indices
        globales para la tabla.

        Permite crear una tabla. Retorna la tabla que se ha creado.
        '''

        tables = self.cnn.list_tables()
        table = Table(table_name, connection=self.cnn)

        #verifica si se debe eliminar una tabla antes de crearla, por ejemplo
        #si la aplicacion  esta ejecuntado un entorno de tests
        if table_name in tables['TableNames'] and table_name.startswith('_'):
            if table.delete():
                tables = self.cnn.list_tables()

        #valida si la tabla ya se encuentra creada.
        if not table_name in tables['TableNames']:
            Table.create(table_name,
                         schema=schema,
                         throughput=throughput,
                         global_indexes=global_indexes,
                         indexes=indexes,
                         connection=self.cnn)
        return table

    def super_create_table_user(self):
        '''
        () -> None

        Permite definir la estructura y posterior creacion de la tabla user.
        '''

        #definicion del esquema de la tabla user.
        schema = [HashKey('key_twitter', data_type=STRING)]

        #definicion del throughput de la tabla user.
        throughput = {'read': 5, 'write': 3}

        #definicion del global index key_user_index de la tabla user.
        key_user_index = GlobalIncludeIndex('key_user_index',
                                parts=[HashKey('key_user', data_type=STRING)],
                                throughput=throughput,
                                includes=['nickname', 'name', 'link_image'])

        #definicion del global index nickname_user_index de la tabla user.
        nickname_user_index = GlobalAllIndex('nickname_user_index',
                                parts=[HashKey('nickname', data_type=STRING)],
                                throughput=throughput)

        table_name = self.TABLE_PREFIX + 'user'

        import dynamoDBqueries

        dynamoDBqueries.table_user = self.create_table(table_name, schema,
                       throughput=throughput,
                       global_indexes=[nickname_user_index, key_user_index])

        self.tables['tbl_user'] = dynamoDBqueries.table_user

    def super_create_table_timeline(self):
        '''
        () -> None

        Permite definir la estructura y posterior creacion de la tabla timeline
        '''

        #definicion del esquema de la tabla timeline.
        schema = [HashKey('key_post', data_type=STRING)]

        #definicion del throughput de la tabla timeline.
        throughput = {'read': 20, 'write': 20}

        #definicion del global index TimelinePublic de la tabla timeline.
        GAI_TimelinePublic = GlobalAllIndex('TimelinePublic',
                        parts=[HashKey('flag_answer', data_type=STRING),
                            RangeKey('key_timeline_post', data_type=STRING)],
                        throughput=throughput)

        #definicion del global index VerTodoPublic de la tabla timeline.
        GAI_VerTodoPublic = GlobalAllIndex('VerTodoPublic',
                        parts=[HashKey('key_post_original', data_type=STRING),
                            RangeKey('key_timeline_post', data_type=STRING)],
                        throughput=throughput)

        #definicion del global index Home de la tabla timeline.
        GAI_Home = GlobalAllIndex('Home',
                        parts=[HashKey('key_user', data_type=STRING),
                            RangeKey('key_timeline_post', data_type=STRING)],
                        throughput=throughput)

        table_name = self.TABLE_PREFIX + 'timeline'

        import dynamoDBqueries

        dynamoDBqueries.table_timeline = self.create_table(table_name, schema, throughput=throughput,
                                  global_indexes=[GAI_TimelinePublic,
                                                  GAI_VerTodoPublic,
                                                  GAI_Home])
        self.tables['tbl_timeline'] = dynamoDBqueries.table_timeline

    def super_create_table_skill(self):
        '''
        () -> None

        Permite definir la estructura y posterior creacion de la tabla skill
        '''

        #definicion del esquema de la tabla skill.
        schema = [HashKey('key_skill', data_type=STRING),
                  RangeKey('key_time', data_type=STRING)]

        #definicion del throughput de la tabla skill.
        throughput = {'read': 5, 'write': 3}

        #definicion del global index GKOI_Navbar de la tabla skill.
        GKOI_Navbar = GlobalKeysOnlyIndex('Navbar',
                        parts=[HashKey('key_user', data_type=STRING),
                            RangeKey('skill', data_type=STRING)],
                        throughput=throughput)

        #definicion del global index GII_Find de la tabla skill.
        GII_Find = GlobalIncludeIndex('Find',
                        parts=[HashKey('skill', data_type=STRING),
                            RangeKey('key_time', data_type=STRING)],
                        throughput=throughput,
                        includes=['key_post'])

        #definicion del global index GII_Post de la tabla skill.
        GII_Post = GlobalIncludeIndex('Post',
                        parts=[HashKey('key_post', data_type=STRING),
                            RangeKey('key_time', data_type=STRING)],
                        throughput=throughput,
                        includes=['skill','key_skill'])
        
        #definicion del global index GKOI_Count de la tabla skill.
        GKOI_Count = GlobalKeysOnlyIndex('Count',
                        parts=[HashKey('skill', data_type=STRING),
                            RangeKey('key_user', data_type=STRING)],
                        throughput=throughput)

        table_name = self.TABLE_PREFIX + 'skill'

        import dynamoDBqueries

        dynamoDBqueries.table_skill = self.create_table(table_name, schema, throughput=throughput,
                            global_indexes=[GKOI_Navbar, GII_Find, GII_Post,GKOI_Count])

        self.tables['tbl_skill'] = dynamoDBqueries.table_skill


class dbTablesTest(dbTables):

    def __init__(self, database):
        super(dbTablesTest, self).__init__(database)

    def create_tables(self):
        '''
        () -> None

        Permite crear todas las tablas necesarias para el entorno de pruebas.
        Las tablas creadas seran llenadas con datos de prueba que se encuentran
        en el archivo test_data.json.
        '''

        #Creacion de las tablas para los test
        super(dbTablesTest, self).create_tables()

        import os
        from commons import jsondecoder

        #cargar los datos de prueba del archivo test_data.json
        path_file = os.path.abspath(self.config['DB_TEST_DATA_PATH'])
        json_data = open(path_file).read()
        data = jsondecoder(json_data)

        #guardar los datos contenidos en el archivo json en la base de datos.
        for key, value in data.items():
            table = self.tables[key]
            for item in value:
                if key == 'tbl_timeline':
                    if 'skills' in item:
                        item['skills'] = set(item['skills'])
                    if 'win_answers' in item:
                        item['win_answers'] = set(item['win_answers'])
                item = Item(table, data=item)
                item.save()

config_db_env = {
    'dev': dbTables,
    'test': dbTablesTest,
    'default': dbTables,
    'aws': dbTablesAWS
}
