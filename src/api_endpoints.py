# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

'''
Created on May 8, 2014

@author: anroco
'''

from flask import Blueprint
from flask.ext import restful
import views_users
import views_timeline
import views_skills

endpoints = Blueprint('endpoints', __name__)

api_version = '/api/1.0'

api = restful.Api(endpoints)

#defir los diferentes endpoints de la aplicacion
api.add_resource(views_users.User, api_version + '/user/')
api.add_resource(views_users.Nickname, api_version + '/user/<string:nickname>')
api.add_resource(views_users.User_scores, api_version + '/auth/user/')
api.add_resource(views_users.Auth_user, api_version + '/login/')
api.add_resource(views_users.User_register, api_version + '/auth/register/')
api.add_resource(views_users.Generate_token, api_version + '/auth/get_token/')

api.add_resource(views_timeline.Timeline_Index, api_version + '/publictimeline')
api.add_resource(views_timeline.Timeline_Answers, api_version + '/allanswers')
api.add_resource(views_timeline.Timeline_Home_Index, api_version + '/home/<string:key>')
api.add_resource(views_timeline.Timeline_QandWinA, api_version + '/post_qwa/<string:key>')
api.add_resource(views_timeline.Timeline_Update, api_version + '/auth/post_q', endpoint='post_q')
api.add_resource(views_timeline.Timeline_Update, api_version + '/auth/post_a', endpoint='post_a')
api.add_resource(views_timeline.Timeline_Update, api_version + '/auth/delete', endpoint='delete_q_a')
api.add_resource(views_timeline.Timeline_Update, api_version + '/auth/update', endpoint='update_q')

api.add_resource(views_skills.Skill_List, api_version + '/findbyskill/<string:skill>', endpoint='findbyskill')
api.add_resource(views_skills.Skill_Update, api_version + '/skills' ,endpoint='updateskills')
api.add_resource(views_skills.Skill_count, api_version + '/totalskills', endpoint='totalskills')






