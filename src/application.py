# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

import os
from flask import Flask
import dynamoDBqueries
from boto.dynamodb2.table import Table
from boto import dynamodb2
from api_endpoints import endpoints
from api_auth import auth

OX_SECRET_KEY = os.environ.get('SECRET_KEY_ANONYMOUS')
OX_TOKEN_USER_LIFETIME = int(os.environ.get('OX_TOKEN_USER_LIFETIME'))
SECRET_KEY_ANONYMOUS = os.environ.get('SECRET_KEY_ANONYMOUS')
TW_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TW_NAME = os.environ.get('TW_NAME')
DEBUG = os.environ.get('FLASK_DEBUG') in ['True', 'true']
TW_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
TW_AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
TW_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TW_BASE_URL = 'https://api.twitter.com/1.1/'


application = Flask(__name__)

application.config.from_object(__name__)

dynamoDBqueries.db_connection = dynamodb2.connect_to_region('us-east-1')
dynamoDBqueries.table_timeline = Table(table_name='timeline',
               connection=dynamoDBqueries.db_connection)
dynamoDBqueries.table_skill = Table(table_name='skill',
               connection=dynamoDBqueries.db_connection)
dynamoDBqueries.table_user = Table(table_name='user',
               connection=dynamoDBqueries.db_connection)

#registrar los blueprints en la application
application.register_blueprint(auth)
application.register_blueprint(endpoints)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
