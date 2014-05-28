'''
Created on May 17, 2014

@author: anroco
'''

from flask import Blueprint, abort, g, request
from flask.ext import restful
from commons import validate_user_auth, user_skills


auth = Blueprint('auth', __name__)
api = restful.Api(auth)
PATHS_EXCEPTION = ['/api/1.0/auth/register/']


@auth.before_app_request
def authentication_user():
    '''
    () -> None

    Se ejecuta cada vez que se realiza una solicitud de recursos de la app.
    Valida si el usuario esta autenticado, verifica si el access_token y
    token_secret generado al autenticarse el usuario con su cuenta de twitter
    es correcto.
    '''

    #verifica si el recurso solicitado necesita que el usuario este autenticado
    if request.method != 'GET' and '/auth/' in request.path:
        user_item = validate_user_auth(request.values['token_user'])
        user_dict = user_skills(user_item._data)

        #verificar si se el usuario ya registro el email y sus habilidades
        #validando todos los path a excepcion de los que se encuentran
        #incluidos en la lista PATHS_EXCEPTION
        if not request.path in PATHS_EXCEPTION and \
            (not 'email' in user_dict or user_dict['email'] == '' or \
             not len(user_dict['skills'])):

            abort(428)

        g.user_item = user_item
        g.user_skills = user_dict['skills']
    else:
        user_item = validate_user_auth(request.values['token_user']
                                       , anonymous=True)
