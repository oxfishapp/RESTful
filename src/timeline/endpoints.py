# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Blueprint
from flask.ext import restful
from views.timeline import (Home_Index
                             , Timeline_Index
                             , AloneView_Index
                             , Timeline_WinAnswers
                             , Timeline_Questions)

endpoints = Blueprint('endpoints',__name__)

api = restful.Api(endpoints)

api.add_resource(Timeline_Index, '/publictimeline')

api.add_resource(AloneView_Index, '/aloneview/<string:key>')

api.add_resource(Home_Index, '/home/<string:key>')

api.add_resource(Timeline_WinAnswers, '/winanswers')

api.add_resource(Timeline_Questions, '/post_q/<string:key>')

api.add_resource(Timeline_Questions, '/post_q',endpoint='post')