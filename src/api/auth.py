'''
Created on May 17, 2014
 
@author: anroco
'''

from flask import Blueprint, abort, g, request
from flask.ext import restful
from commons import twitter_credentials

auth = Blueprint('auth',__name__)


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
        user_tiwtter = twitter_credentials(request.values['access_token']
                                                    ,request.values['token_secret'] 
                                                    ,g.tw_auth)
        #valida la respuesta dada por twitter.  
        if user_tiwtter.status != 200:
            abort(401)
        g.id_twitter = user_tiwtter.data['id_str']

#Registro de la funcion que permitira conocer si un usuario esta autenticado.
auth.before_app_request(authentication_user)

api = restful.Api(auth)
