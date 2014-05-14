from flask import Blueprint
from flask.ext import restful
from views.timeline import (Home_Index
                             , Timeline_Index
                             , AloneView_Index
                             , WinAnswers_Table)

endpoints = Blueprint('Blueprint',__name__)

api = restful.Api(endpoints)

api.add_resource(Timeline_Index, '/publictimeline')
api.add_resource(AloneView_Index, '/aloneview/<string:hashKey>')
api.add_resource(Home_Index, '/home/<string:hashKey>')
api.add_resource(WinAnswers_Table, '/winanswers')