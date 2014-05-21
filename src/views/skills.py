# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from application import dynamodb
from flask.ext.restful import Resource, reqparse, marshal_with
from formats import format_skill

db_connection = dynamodb.db_connection
table = dynamodb.tables['tbl_skills']

#Se Ingresan los datos luego que
#un usuario se registre
#se consulta para poner las habilidades
#en el navigation bar
class Skill_Navbar_Index(Resource):
    pass

#Se ingresa los datos cuando se realiza 
#una pregunta
#se consulta cuando se hace un click en skills
class Skill_Table(Resource):
    pass