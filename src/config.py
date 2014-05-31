# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

'''
Created on May 10, 2014

@author: anroco
'''


class AppConfig:

    TYPE = 'DEV'
    SERVER_NAME = 'localhost:5000'
    OX_SECRET_KEY = "kEv7FEBT8rarwB41Hf72Bw50HbY6dyOU4CiwXHkFdExs5NgVQWaray6civgs4aYX"
    SECRET_KEY_ANONYMOUS = 'YGWF5VLNhwduPtfMisczxgYDWRqoG5bW'
    DB_HOST = 'localhost'
    DB_PORT = 8000
    DB_AWS_ACCESS_KEY_ID = 'DEVDB'
    DB_AWS_SECRET_KEY = 'DEVDB'
    DB_IS_SECURE = False
    DB_TABLE_PREFIX = ''
    DB_LIMIT = 10
    TW_CONSUMER_KEY = 'QbINcoPerlOi4Y4QD3wSjHJKp'
    TW_CONSUMER_SECRET = 'ZBR4eNAo6KUK0gnZO2vm2JKLZdU4gh3DVbcnSibC42diBz1fiJ'
    TW_NAME = 'restanroco'
    TW_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    TW_AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
    TW_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    TW_BASE_URL = 'https://api.twitter.com/1.1/'


class AppConfigAWS(AppConfig):

#    import os

     TYPE = 'AWS'
#     FLASK_DEBUG = os.environ.get('FLASK_DEBUG') if os.environ.get('FLASK_DEBUG') else False
#     SERVER_NAME = os.environ.get('SERVER_NAME') if os.environ.get('SERVER_NAME') else '0.0.0.0:5000'
#     OX_SECRET_KEY = os.urandom(64)
#     DB_LIMIT = os.environ.get('DB_LIMIT') if os.environ.get('DB_LIMIT') else 5
#     TW_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY') if os.environ.get('TW_CONSUMER_KEY') else None
#     TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET') if os.environ.get('TW_CONSUMER_SECRET') else None
#     TW_NAME = os.environ.get('TW_NAME') if os.environ.get('TW_NAME') else 'OxfishRESTful'


class DevConfig(AppConfig):
    TYPE = 'DEV'
    DEBUG = True
    DEBUG_WITH_APTANA = True
    DB_TABLE_PREFIX = '_dev_'
    DB_TEST_DATA_PATH = 'tests/test_data.json'


class TestConfig(AppConfig):
    TYPE = 'TEST'
    TESTING = True
    DB_TABLE_PREFIX = '_test_'
    DB_TEST_DATA_PATH = 'test_data.json'


config_env = {
    'dev': DevConfig,
    'test': TestConfig,
    'default': AppConfig,
    'aws': AppConfigAWS
}
