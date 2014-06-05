# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Flask
from config import config_env
from dynamoDB import config_db_env

application = Flask(__name__)

def create_app(config_type):
    """(str) -> Flask

    Crea y retorna la aplicacion teniendo en cuenta el tipo de
    configuracion deseada.
    """
    application.config.from_object(config_env[config_type])
    config = application.config
    db_tables = config_db_env[config_type](config)
    db_tables.create_tables()

    #registrar los blueprints en la application
    from api_endpoints import endpoints
    from api_auth import auth

    application.register_blueprint(endpoints)
    application.register_blueprint(auth)

    return application

if __name__ == "__main__":

    application = create_app('dev')

    #valida si la aplicacion se inicializa en modo debug y el debug se hace
    #por medio de un tercero(Eclipse, Aptana).
    if application.debug and 'DEBUG_WITH_APTANA' in application.config:
        uso_debug = not (application.config.get('DEBUG_WITH_APTANA'))

    application.run(use_debugger=uso_debug, debug=application.debug,
                    use_reloader=uso_debug, host='0.0.0.0')

# curl http://localhost:5000/api/1.0/publictimeline
# curl http://localhost:5000/api/1.0/home/fedcf7af-e9f0-69cc-1c68-362d8f5164ea
# curl http://localhost:5000/api/1.0/winanswers -d 'HashKeyList=["31EC2020-3AEA-4069-A2DD-08002B30309D"]' -X GET
# curl http://localhost:5000/api/1.0/post_q/11EC2020-3AEA-4069-A2DD-08002B30309D
# curl http://localhost:5000/api/1.0/aloneview -d 'HashKey=11EC2020-3AEA-4069-A2DD-08002B30309D' -X GET
# curl http://oxrestful-env-xhpkmpkmpt.elasticbeanstalk.com/api/1.0/auth/post_q -d 'jsontimeline={"message140": "Howto Create a table with Python in dynamoDB from Flask?", "source": "Web", "Geolocation": "4.598056,-74.075833", "skills": ["flask", "python", "dynamodb"], "link": "Http://Imagen de Pregunta", "key_user": "c19456aa-6fb3-4f27-915a-697b612cdb2f"}' -X POST
# curl http://localhost:5000/api/1.0/post_a -d 'JsonTimeline={"Message140": "Howto Create a table with Python in dynamoDB from Flask?", "Source": "Web", "Geolocation": "4.598056,-74.075833", "Link": "Imagen de Pregunta", "Key_User": "AEAF8765-4069-4069-A2DD-08002B30309D","Key_PostOriginal" : "11EC2020-3AEA-4069-A2DD-08002B30309D"}' -X POST
# curl http://oxrestful-env-xhpkmpkmpt.elasticbeanstalk.com/api/1.0/auth/delete -d 'hash_key=0fb4cf4f-240f-44ed-9f20-3ce99954c414' -X DELETE -v
# curl http://localhost:5000/api/1.0/update -d 'HashKey=722ae3bc-7e1c-aa3d-18c6-a95c028f1c8c' -d 'JsonTimeline={"TotalAnswers" : 1}' -X PUT
# curl http://localhost:5000/api/1.0/update -d 'HashKey=722ae3bc-7e1c-aa3d-18c6-a95c028f1c8c' -d 'JsonTimeline={"WinAnswers" : {"State" : 1, "HashKey" : "02016600-6f94-4749-b225-040018f7eb19"}}' -X PUT

#         {"WinAnswers" : {"State" : 1, "HashKey" : "02016600-6f94-4749-b225-040018f7eb19"}}


#curl http://localhost:5000/api/1.0/auth/user/ -d "access_token=85721956-EFmG1NywpV3VEMDnMDbNax9JJ4OfFvEsCLKWi4Slq" -d "token_secret=FnDmaaBBzZceF3whMsZom9BmKpUFfyuRNFuBKJHXngZMf" -d "post=false" -d "answer=true" -X PUT


#{
#'Key_Post'          : '21EC2020-3AEA-4069-A2DD-08002B30309D'
#,'Key_TimelinePost' : '2014-05-14 17:24:31'
#,'Geolocation'      : '4.598056,-74.075833'
#,'Source'           : 'Web'
#,'Message140'       : 'UNO link del video mas respuesta del usuario'
#,'Key_User'         : 'BEAF8765-4069-4069-A2DD-08002B30309D'
#,'Key_PostOriginal' : '11EC2020-3AEA-4069-A2DD-08002B30309D'
#,'Link'             : 'link video'
#}
