# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Flask
from endpoints import endpoints

app = Flask(__name__)

app.register_blueprint(endpoints)

if __name__ == '__main__':
    app.run(debug=True)

# curl http://localhost:5000/publictimeline
# curl http://localhost:5000/home/AEAF8765-4069-4069-A2DD-08002B30309D
# curl http://localhost:5000/winanswers -d 'HashKeyList=["31EC2020-3AEA-4069-A2DD-08002B30309D"]' -X GET
# curl http://localhost:5000/post_q/11EC2020-3AEA-4069-A2DD-08002B30309D
# curl http://localhost:5000/aloneview -d 'HashKey=11EC2020-3AEA-4069-A2DD-08002B30309D' -X GET
# curl http://localhost:5000/post_q -d 'JsonTimeline={"Message140": "Howto Create a table with Python in DynamoDB from Flask?", "Source": "Web", "Geolocation": "4.598056,-74.075833", "Tags": ["Flask", "Python", "DynamoDB"], "Link": "Imagen de Pregunta", "Key_User": "AEAF8765-4069-4069-A2DD-08002B30309D"}' -X POST
# curl http://localhost:5000/post_a -d 'JsonTimeline={"Message140": "Howto Create a table with Python in DynamoDB from Flask?", "Source": "Web", "Geolocation": "4.598056,-74.075833", "Link": "Imagen de Pregunta", "Key_User": "AEAF8765-4069-4069-A2DD-08002B30309D","Key_PostOriginal" : "11EC2020-3AEA-4069-A2DD-08002B30309D"}' -X POST
# curl http://localhost:5000/delete -d 'HashKey=8c0b8e8e-8b5a-f8f8-0684-21b76bf61293' -X DELETE -v
# curl http://localhost:5000/update -d 'HashKey=722ae3bc-7e1c-aa3d-18c6-a95c028f1c8c' -d 'JsonTimeline={"TotalAnswers" : 1}' -X PUT
# curl http://localhost:5000/update -d 'HashKey=722ae3bc-7e1c-aa3d-18c6-a95c028f1c8c' -d 'JsonTimeline={"WinAnswers" : {"State" : 1, "HashKey" : "02016600-6f94-4749-b225-040018f7eb19"}}' -X PUT

#         {"WinAnswers" : {"State" : 1, "HashKey" : "02016600-6f94-4749-b225-040018f7eb19"}}

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