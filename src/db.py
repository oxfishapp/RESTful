'''
Created on May 9, 2014

@author: anroco
'''

from boto.dynamodb2.layer1 import DynamoDBConnection

class Singleton(object):
    '''
    definicion de la clase de modo singleton.    
    '''
    
    __instance = None
    
    #override del metodo __new __ que permite crear una sola instancia
    #respetando el patron de diseno singleton 
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

class DynamoDB(Singleton):
    '''
    permite gestionar la conexion a la base de datos dynamoDB
    '''
    
    #objeto para manejar la conexion a la base de datos
    db_connection = None
    
    #configuracion definida para la aplicacion archivo config.py
    config = None
    
    #diccionario con la lista de tablas
    tables = {}
    
    def connect(self, config):
        '''
        (str) -> NoneType
        
        permite crear la conexion a la base de datos de acuerdo a la 
        configuracion deseada.
        '''
        
        if self.db_connection is None:
            self.config = config
            self.db_connection = DynamoDBConnection(
                host = self.config.DB_HOST,
                port = self.config.DB_PORT,
                aws_access_key_id = self.config.DB_AWS_ACCESS_KEY_ID,
                aws_secret_access_key = self.config.DB_AWS_SECRET_KEY,
                is_secure = self.config.DB_IS_SECURE)
        
    
    def disconnect(self):
        '''
        () -> NoneType
        
        termina la conexion a la base de datos.
        '''
        
        self.db_connection.close()
        