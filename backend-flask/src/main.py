# -*- coding:utf-8 -*- 
from pprint import pprint 
from flask import Flask,abort
from flask import request
from flask_restful import Api

#from apiRoute.affair import *
from apiRoute.login import *


app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/static/<file_name>')
def static_file_request(file_name):
    return app.send_static_file(f'static/{file_name}')

##
## Backend API
##
api.add_resource(User, '/user')
api.add_resource(Login, '/login')

##
## Item&Affairs API
##

#api.add_resource(Affair, '/affair/<string:affair_id>')
#api.add_resource(Login, '/item/<string:affair_id>')

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8080)
