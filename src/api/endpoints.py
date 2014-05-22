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
from views import timeline
from views import skills

endpoints = Blueprint('endpoints',__name__)

api_version = '/api/1.0'

api = restful.Api(endpoints)

#defir los diferentes endpoints de la aplicacion
api.add_resource(users.User, api_version +  '/user/')
api.add_resource(users.Nickname, api_version +  '/user/<string:nickname>')
api.add_resource(users.User_post, api_version + '/post/user/')
api.add_resource(users.User_scores, api_version + '/auth/user/')
api.add_resource(users.Auth_user, api_version + '/login/')
api.add_resource(users.User_register, api_version + '/auth/register/')

api.add_resource(timeline.Timeline_Index, api_version + '/publictimeline')
api.add_resource(timeline.Timeline_Answers, api_version + '/aloneview')
api.add_resource(timeline.Timeline_Home_Index, api_version + '/home/<string:key>')
api.add_resource(timeline.Timeline_WinAnswers, api_version + '/winanswers')
api.add_resource(timeline.Timeline_Questions, api_version + '/post_q/<string:key>')
api.add_resource(timeline.Timeline_Update, api_version + '/auth/post_q', endpoint='post_q')
api.add_resource(timeline.Timeline_Update, api_version + '/auth/post_a', endpoint='post_a')
api.add_resource(timeline.Timeline_Update, api_version + '/auth/delete', endpoint='delete_q_a')
api.add_resource(timeline.Timeline_Update, api_version + '/auth/update', endpoint='update_q')

api.add_resource(skills.Skill_Table, api_version + '/finderskill', endpoint='finderskill')
