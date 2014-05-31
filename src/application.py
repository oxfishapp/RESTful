# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Flask
from config import config_env
import dynamoDBqueries
from boto.dynamodb2.table import Table
from boto import dynamodb2
from api_endpoints import endpoints
from api_auth import auth

application = Flask(__name__)

dynamoDBqueries.db_connection = dynamodb2.connect_to_region('us-east-1')
#                         aws_access_key_id='AKIAJ4MQ2TCTX3UAE6AQ',
#                         aws_secret_access_key='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')
dynamoDBqueries.table_timeline = Table(table_name='timeline',
               connection=dynamoDBqueries.db_connection)
dynamoDBqueries.table_skill = Table(table_name='skill',
               connection=dynamoDBqueries.db_connection)
dynamoDBqueries.table_user = Table(table_name='user',
               connection=dynamoDBqueries.db_connection)

application.config.from_object(config_env['aws'])

#registrar los blueprints en la application
application.register_blueprint(endpoints)
#application.register_blueprint(auth)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
