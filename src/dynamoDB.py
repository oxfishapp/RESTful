from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import (GlobalIncludeIndex, GlobalAllIndex,
                                   GlobalKeysOnlyIndex)
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import STRING


class dbTables(object):

    def __init__(self, database):
        '''
        (boto.dynamodb2.layer1.DynamoDBConnection) -> None

        Inicializa el objeto dbTables el cual permitira realizar el proceso
        de creacion de las tablas de la aplicacion.
        '''

        self.dynamodb = database
        self.TABLE_PREFIX = database.config.DB_TABLE_PREFIX
        self.db_connection = database.db_connection

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

        tables = self.db_connection.list_tables()
        table = Table(table_name, connection=self.db_connection)

        #verifica si se debe eliminar una tabla antes de crearla, por ejemplo
        #si la aplicacion  esta ejecuntado un entorno de tests
        if table_name in tables['TableNames'] and table_name.startswith('_'):
            if table.delete():
                tables = self.db_connection.list_tables()

        #valida si la tabla ya se encuentra creada.
        if not table_name in tables['TableNames']:
            Table.create(table_name,
                         schema=schema,
                         throughput=throughput,
                         global_indexes=global_indexes,
                         indexes=indexes,
                         connection=self.db_connection)
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
        table = self.create_table(table_name, schema, throughput=throughput,
                          global_indexes=[nickname_user_index, key_user_index])
        self.dynamodb.tables['tbl_user'] = table

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
        table = self.create_table(table_name, schema, throughput=throughput,
                                  global_indexes=[GAI_TimelinePublic,
                                                  GAI_VerTodoPublic,
                                                  GAI_Home])
        self.dynamodb.tables['tbl_timeline'] = table

    def super_create_table_skill(self):
        '''
        () -> None

        Permite definir la estructura y posterior creacion de la tabla skill
        '''

        #definicion del esquema de la tabla skill.
        schema = [HashKey('skill', data_type=STRING),
                  RangeKey('key_time', data_type=STRING)]

        #definicion del throughput de la tabla skill.
        throughput = {'read': 5, 'write': 3}

        #definicion del global index GKOI_Navbar de la tabla skill.
        GKOI_Navbar = GlobalKeysOnlyIndex('GKOI_Navbar',
                        parts=[HashKey('key_user', data_type=STRING),
                            RangeKey('skill', data_type=STRING)],
                        throughput=throughput)

        #definicion del global index GII_Find de la tabla skill.
        GII_Find = GlobalIncludeIndex('GII_Find',
                        parts=[HashKey('skill', data_type=STRING),
                            RangeKey('key_time', data_type=STRING)],
                        throughput=throughput,
                        includes=['key_post'])

        #definicion del global index GII_Post de la tabla skill.
        GII_Post = GlobalIncludeIndex('GII_Post',
                        parts=[HashKey('key_post', data_type=STRING),
                            RangeKey('key_time', data_type=STRING)],
                        throughput=throughput,
                        includes=['skill'])

        table_name = self.TABLE_PREFIX + 'skill'
        table = self.create_table(table_name, schema, throughput=throughput,
                            global_indexes=[GKOI_Navbar, GII_Find, GII_Post])
        self.dynamodb.tables['tbl_skills'] = table


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
        path_file = os.path.abspath(self.dynamodb.config.DB_TEST_DATA_PATH)
        json_data = open(path_file).read()
        data = jsondecoder(json_data)

        #guardar los datos contenidos en el archivo json en la base de datos.
        for key, value in data.items():
            table = self.dynamodb.tables[key]
            for item in value:
                if key == 'tbl_timeline':
                    if 'skills' in item:
                        item['skills'] = set(item['skills'])
                    if 'win_answers' in item:
                        item['win_answers'] = set(item['win_answers'])
                item = Item(table, data=item)
                item.save()

config_db_env = {
    'dev': dbTablesTest,
    'test': dbTablesTest,
    'default': dbTables
}
