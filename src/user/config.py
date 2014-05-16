'''
Created on May 10, 2014

@author: anroco
'''

class Config:
    
    SERVER_NAME = 'localhost:5000'
    DB_HOST = 'localhost'
    DB_PORT = 8000
    DB_AWS_ACCESS_KEY_ID = 'DEVDB'
    DB_AWS_SECRET_KEY = 'DEVDB'
    DB_IS_SECURE = False
    DB_TABLE_SUFFIX = ''
    
    @staticmethod
    def iniciar_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    DEBUG_WITH_APTANA = True


class TestConfig(Config):
    TESTING = True
    DB_TABLE_SUFFIX = '_test_'


config_env = {
    'dev': DevConfig,
    'test': TestConfig,
    'default': DevConfig
}