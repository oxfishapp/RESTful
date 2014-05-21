'''
Created on May 9, 2014

@author: anroco
'''

from flask import Flask
from user.config import config_env
from user.DBtables import config_db_env
from user.app.db import DynamoDB
from flask_oauth import OAuth


dynamodb = DynamoDB()

def create_app(config_type):
    """(str) -> Flask
    
    Crea y retorna la aplicacion teniendo en cuenta el tipo de configuracion deseada.
    
    """

    app = Flask(__name__)
    config = config_env[config_type]
    app.config.from_object(config)
    dynamodb.connect(config)
    db_tables = config_db_env[config_type](dynamodb)
    db_tables.create_tables()

    
    #registrar los blueprints en la app
    from user.app.api.endpoints import endpoints
    from user.app.api.auth import auth
    
    app.register_blueprint(endpoints)
    app.register_blueprint(auth)
    
    #Flask OAuth para acceder al login de twitter
    tw_auth = OAuth().remote_app(name=config.TW_NAME
                               ,base_url=config.TW_BASE_URL
                               ,request_token_url=config.TW_REQUEST_TOKEN_URL
                               ,access_token_url=config.TW_ACCESS_TOKEN_URL
                               ,authorize_url=config.TW_AUTHORIZE_URL
                               ,consumer_key=config.TW_CONSUMER_KEY
                               ,consumer_secret=config.TW_CONSUMER_SECRET)

    app_ctx = app.app_context()
    app_ctx.g.tw_auth = tw_auth
    app_ctx.push()
    
    import os
    app.secret_key = os.urandom(64)
    
    return app



if __name__ == "__main__":
    
    app = create_app('dev')
    
    #valida si la aplicacion se inicializa en modo debug y el debug se hace
    #por medio de un tercero(Eclipse, Aptana).
    if app.debug and app.config.has_key('DEBUG_WITH_APTANA'):
        uso_debug = not (app.config.get('DEBUG_WITH_APTANA'))
    

    
    app.run(use_debugger=uso_debug, debug=app.debug
            , use_reloader=uso_debug, host='192.168.0.91', port=8080)
    