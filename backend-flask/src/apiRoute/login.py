# -*- coding:utf-8 -*- 
import pprint
import sys
import threading
from flask import Flask,abort
from flask_restful import reqparse, Resource, reqparse
from dataModel import user_data

sys.path.append("..")
from config.backend_conf import CONFIG_DB,USER_TABLE

#用户表锁
USER_TABLE_LOCK = threading.Lock()

#用户属性参数校验
def user_prop(prop_str):
    if prop_str not in User.PropType:
        raise ValidationError("{} is not a valid user prop")
    else:
        return True

#用户相关操作
class User(Resource):
    #用户属性
    PropType = ["administrators",
                "controller",
                "normalizer"]

    #根据时间范围,获取当前事务列表
    def get(self):
        # 查询是否存在超级用户
        USER_TABLE_LOCK.acquire()
        ret = user_data.User(CONFIG_DB,USER_TABLE).has_super_user()
        USER_TABLE_LOCK.release()
        return {"hasSuperUser": ret}, 200

    #删除一条事务记录
    def delete(self):
        # 增加用户
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('username', dest='username',
                                 type=str, location='json',
                                 required=True, help='Need input username for user add.')
        
        req = put_parser.parse_args()

        USER_TABLE_LOCK.acquire()
        ret = user_data.User(CONFIG_DB,USER_TABLE).user_delete(**req)
        USER_TABLE_LOCK.release()

        if not ret:
            return '{"message":"删除失败,无此用户"}', 200
        else:
            return '{"message":"删除成功"}', 200
    
    #完成事务的修改和添加
    def post(self):
        # 增加用户
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
        ret = user_data.User(CONFIG_DB,USER_TABLE).user_add(**req)
        USER_TABLE_LOCK.release()

        if not ret:
            abort(503)
        else:
            return "",200

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
        ret,prop = user_data.User(CONFIG_DB,USER_TABLE).user_check(**req)
        USER_TABLE_LOCK.release()

        if not ret:
            return '{"message":"用户密码错误"}',200 
        else:
            return f'{{"message":"登陆成功","user_prop":"{prop}"}}',200 


#用户管理模块单元测试
if __name__ == '__main__':
    pass





