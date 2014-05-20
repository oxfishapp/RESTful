# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Blueprint
from flask.ext import restful
from views.timeline import (Home_Index
                             , Timeline_Index
                             , Timeline_Answers
                             , Timeline_WinAnswers
                             , Timeline_Questions
                             , Timeline_Update)

endpoints = Blueprint('Blueprint',__name__)

api = restful.Api(endpoints)

api.add_resource(Timeline_Index, '/publictimeline')

api.add_resource(Timeline_Answers, '/aloneview')

api.add_resource(Home_Index, '/home/<string:key>')

api.add_resource(Timeline_WinAnswers, '/winanswers')

api.add_resource(Timeline_Questions, '/post_q/<string:key>')

api.add_resource(Timeline_Update, '/post_q',endpoint='post_q')

api.add_resource(Timeline_Update, '/post_a', endpoint='post_a')

api.add_resource(Timeline_Update, '/delete', endpoint='delete_q_a')

api.add_resource(Timeline_Update, '/update', endpoint='update_q')