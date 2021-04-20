# -*- coding:utf-8 -*- 
import pprint
import sys
import threading
from flask import Flask,abort
from flask_restful import reqparse, Resource, reqparse
from dataModel import user_data

#用户表锁
USER_TABLE_LOCK = threading.Lock()

#用户属性参数校验
def user_prop(prop_str):
    if prop_str not in User.PropType:
        raise ValidationError("{} is not a valid user prop")
    else:
        return prop_str

#用户相关操作
class User(Resource):
    #用户属性
    PropType = ["administrators",
                "controller",
                "normalizer"]

    #根据时间范围,获取当前事务列表
    def get(self):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('ischeck_super', dest='ischeck_super',
                                 type=bool, location='args',
                                 required=False)
        req = put_parser.parse_args()

        if req["ischeck_super"]:
            # 查询是否存在超级用户
            USER_TABLE_LOCK.acquire()
            ret = user_data.UserData().has_super_user()
            USER_TABLE_LOCK.release()
            return {"hasSuperUser": ret}, 200
        else:
            # 查询普通用户
            USER_TABLE_LOCK.acquire()
            ret = user_data.UserData().get_user()
            USER_TABLE_LOCK.release()
            # 按照密码是否存在修改
            for user in ret:
                if user["user_passwd"]:
                    user["user_passwd"] = True
                else:
                    user["user_passwd"] = False
            return ret, 200

    #删除用户
    def delete(self):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('username', dest='username',
                                 type=str, location='json',
                                 required=True, help='Need input username for user add.')
        
        req = put_parser.parse_args()

        USER_TABLE_LOCK.acquire()
        ret = user_data.UserData().user_delete(**req)
        USER_TABLE_LOCK.release()

        if not ret:
            return '{"message":false}', 200
        else:
            return '{"message":true}', 200
    
    # 增加用户
    def put(self):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('username', dest='username',
                                 type=str, location='json',
                                 required=True, help='Need input username for user add.')
        put_parser.add_argument('prop', dest='prop',
                                 type=user_prop, location='json',
                                 required=True, help='User prop should be one of ["administrators","controller","normalizer"].')
        put_parser.add_argument('passwd', dest='passwd',
                                 type=str, location='json',
                                 required=True, help='Need input passwd for user add.')
        req = put_parser.parse_args()

        USER_TABLE_LOCK.acquire()
        ret = user_data.UserData().user_add(**req)
        USER_TABLE_LOCK.release()

        if not ret:
            abort(503)
        else:
            return {'ret':True},200

#登陆相关操作
class Login(Resource):
    def put(self):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('username', dest='username',
                                  type=str, location='json',
                                  required=True, help='Need input username for user check.')
        put_parser.add_argument('passwd', dest='passwd',
                                 type=str, location='json',
                                 required=True, help='Need input passwd for user check.')
        req = put_parser.parse_args()

        # 登陆,校验用户,返回用户特征,加锁
        USER_TABLE_LOCK.acquire()
        ret,prop = user_data.UserData().user_check(**req)
        USER_TABLE_LOCK.release()

        if not ret and prop == '':
            return {"ret":False,"message":"用户密码错误"},200 
        elif not ret and prop != '':
            return {"ret":True,"message":"无初始化","user_prop":prop},200 
        else:
            return {"ret":True,"message":"登陆成功","user_prop":prop},200 


#用户管理模块单元测试
if __name__ == '__main__':
    pass





