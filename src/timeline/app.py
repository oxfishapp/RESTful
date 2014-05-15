# -*- coding: utf-8 -*-
#!/usr/bin/env python
#!flask/bin/python

from flask import Flask
from endpoints import endpoints

app = Flask(__name__)

app.register_blueprint(endpoints)

if __name__ == '__main__':
    app.run(debug=True)
    
#curl http://localhost:5000/winanswers -d 'HashKeyList=["31EC2020-3AEA-4069-A2DD-08002B30309D"]' -X GET
#curl http://localhost:5000/home/AEAF8765-4069-4069-A2DD-08002B30309D
#curl http://localhost:5000/aloneview/11EC2020-3AEA-4069-A2DD-08002B30309D  
#curl http://localhost:5000/publictimeline
#curl http://localhost:5000/post_q/11EC2020-3AEA-4069-A2DD-08002B30309D
#curl http://localhost:5000/post_q -d 'JsonTimeline={"Message140": "Howto Create a table with Python in DynamoDB from Flask?", "Source": "Web", "Geolocation": "4.598056,-74.075833", "Tags": ["Flask", "Python", "DynamoDB"], "Link": "Imagen de Pregunta", "Key_User": "AEAF8765-4069-4069-A2DD-08002B30309D"}' -X POST
