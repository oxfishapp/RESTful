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

apiapplication = restful.Api(endpoints)



#defir los diferentes endpoints de la aplicacion
apiapplication.add_resource(views_users.User, api_version + '/user/')
apiapplication.add_resource(views_users.Nickname, api_version + '/user/<string:nickname>')
apiapplication.add_resource(views_users.User_scores, api_version + '/auth/user/')
apiapplication.add_resource(views_users.Auth_user, api_version + '/login/')
apiapplication.add_resource(views_users.User_register, api_version + '/auth/register/')
apiapplication.add_resource(views_users.Generate_token, api_version + '/auth/get_token/')

apiapplication.add_resource(views_timeline.Timeline_Index, api_version + '/publictimeline')
apiapplication.add_resource(views_timeline.Timeline_Answers, api_version + '/allanswers')
apiapplication.add_resource(views_timeline.Timeline_Home_Index, api_version + '/home/<string:key>')
apiapplication.add_resource(views_timeline.Timeline_QandWinA, api_version + '/post_qwa/<string:key>')
apiapplication.add_resource(views_timeline.Timeline_Update, api_version + '/auth/post_q', endpoint='post_q')
apiapplication.add_resource(views_timeline.Timeline_Update, api_version + '/auth/post_a', endpoint='post_a')
apiapplication.add_resource(views_timeline.Timeline_Update, api_version + '/auth/delete', endpoint='delete_q_a')
apiapplication.add_resource(views_timeline.Timeline_Update, api_version + '/auth/update', endpoint='update_q')

apiapplication.add_resource(views_skills.Skill_List, api_version + '/findbyskill/<string:skill>', endpoint='findbyskill')
apiapplication.add_resource(views_skills.Skill_Update, api_version + '/skills' ,endpoint='updateskills')
apiapplication.add_resource(views_skills.Skill_count, api_version + '/totalskills', endpoint='totalskills')






