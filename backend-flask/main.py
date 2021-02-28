# -*- coding:utf-8 -*- 
from pprint import pprint 
from flask import Flask,abort
from flask import request
from module.login import global_login

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/static/<file_name>')
def static_file_request(file_name):
    return app.send_static_file(f'static/{file_name}')

@app.route('/user', methods=['POST', 'GET', 'PUT'])
def user():
    if request.method == 'GET':
        # 查询是否存在超级用户
        return {"hasSuperUser": global_login.HasSuperUser()}, 200

    elif request.method == 'POST':
        # 增加用户
        ret = global_login.UserAdd({"username":request.json["username"],
                                    "prop":request.json["prop"],
                                    "passwd":request.json["passwd"]})

        if not ret:
            abort(503)
        else:
            return "",200

    elif request.method == 'PUT':
        # 修改密码
        return

    abort(501)

@app.route('/login', methods=['PUT'])
def login():
    if request.method == 'PUT':
        # 登陆
        

        return None, 200

    abort(501)

'''
@app.errorhandler(401)
def page_unauthorized(error):
    return render_template_string('<h1> Unauthorized </h1><h2>{{ error_info }}</h2>', error_info=error), 401
'''

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8080)
