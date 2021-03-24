# -*- coding:utf-8 -*- 
from pprint import pprint 
from flask import Flask,abort
from flask import request
from flask_restful import Api

#from apiRoute.affair import *
from apiRoute.login import *
from apiRoute.affair import *

from dataModel.model_version import DataVersion
from dataModel.affairs_data import AffairContent,AffairList
from dataModel.user_data import UserData

app = Flask(__name__,static_url_path='/static',static_folder='../static')
api = Api(app)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/static/<file_name>')
def static_file_request(file_name):
    return app.send_static_file(f'{file_name}')

##
## Backend API
##
api.add_resource(User, '/user')
api.add_resource(Login, '/login')

##
## Item&Affairs API
##
api.add_resource(Affairs,'/affair')
api.add_resource(AffairsContent,'/affair/<string:affair_id>')

if __name__ == '__main__':
    #update Data Model
    DataVersion(AffairList(),AffairContent(),UserData())
    app.run(debug=True,host='127.0.0.1',port=8080)
