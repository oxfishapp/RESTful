# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

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
    TW_CONSUMER_KEY = 'QbINcoPerlOi4Y4QD3wSjHJKp'
    TW_CONSUMER_SECRET = 'ZBR4eNAo6KUK0gnZO2vm2JKLZdU4gh3DVbcnSibC42diBz1fiJ'
    TW_NAME = 'restanroco'
    TW_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    TW_AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
    TW_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    TW_BASE_URL = 'https://api.twitter.com/1.1/'
    
    
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