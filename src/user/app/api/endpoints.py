'''
Created on May 8, 2014

@author: anroco
'''

from flask import Blueprint
from flask.ext import restful
from ..views import users

endpoints = Blueprint('endpoint',__name__)

api = restful.Api(endpoints)

#defir los diferentes endpoints de la aplicacion
api.add_resource(users.User, '/user/')
api.add_resource(users.User_post, '/post/user/')
api.add_resource(users.User_scores, '/auth/user/')
api.add_resource(users.Auth_user, '/login/')

