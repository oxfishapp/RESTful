# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Flask
#from config import config_env
import dynamoDBqueries
from boto.dynamodb2.table import Table
from boto import dynamodb2
from api_endpoints import endpoints
from api_auth import auth

#SERVER_NAME = 'localhost:5000'
OX_SECRET_KEY = "kEv7FEBT8rarwB41Hf72Bw50HbY6dyOU4CiwXHkFdExs5NgVQWaray6civgs4aYX"
SECRET_KEY = 'kEv7FEBT8rarwB41Hf72Bw50HbY6dyOU4CiwXHkFdExs5NgVQWaray6civgs4aYX'
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


application = Flask(__name__)

application.config.from_object(__name__)

dynamoDBqueries.db_connection = dynamodb2.connect_to_region('us-east-1')
#                         aws_access_key_id='AKIAJ4MQ2TCTX3UAE6AQ',
#                         aws_secret_access_key='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')
dynamoDBqueries.table_timeline = Table(table_name='timeline',
               connection=dynamoDBqueries.db_connection)
dynamoDBqueries.table_skill = Table(table_name='skill',
               connection=dynamoDBqueries.db_connection)
dynamoDBqueries.table_user = Table(table_name='user',
               connection=dynamoDBqueries.db_connection)

#application.config.from_object(config_env['aws'])

#registrar los blueprints en la application
application.register_blueprint(endpoints)
application.register_blueprint(auth)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
