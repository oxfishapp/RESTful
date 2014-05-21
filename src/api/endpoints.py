# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

'''
Created on May 8, 2014

@author: anroco
'''

from flask import Blueprint
from flask.ext import restful
from views import users
from flask import Blueprint
from flask.ext import restful
from views.timeline import (   Timeline_Home_Index
                             , Timeline_Index
                             , Timeline_Answers
                             , Timeline_WinAnswers
                             , Timeline_Questions
                             , Timeline_Update)

endpoints = Blueprint('endpoints',__name__)

api_version = '/api/1.0'

api = restful.Api(endpoints)

#defir los diferentes endpoints de la aplicacion
api.add_resource(users.User,  '/user/')
api.add_resource(users.User_post, '/post/user/')
api.add_resource(users.User_scores, '/auth/user/')
api.add_resource(users.Auth_user, '/login/')


api.add_resource(Timeline_Index, api_version + '/publictimeline')

api.add_resource(Timeline_Answers, api_version + '/aloneview')

api.add_resource(Timeline_Home_Index, api_version + '/home/<string:key>')

api.add_resource(Timeline_WinAnswers, api_version + '/winanswers')

api.add_resource(Timeline_Questions, api_version + '/post_q/<string:key>')

api.add_resource(Timeline_Update, api_version + '/post_q', endpoint='post_q')

api.add_resource(Timeline_Update, api_version + '/post_a', endpoint='post_a')

api.add_resource(Timeline_Update, api_version + '/delete', endpoint='delete_q_a')

api.add_resource(Timeline_Update, api_version + '/update', endpoint='update_q')

