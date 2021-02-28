# -*- coding:utf-8 -*- 
import sqlite3
import pprint
import sys
from flask import current_app

sys.path.append("../..")
from config.backend_conf import CONFIG_DB,USER_TABLE

#用户对象
class User(object):
    prop_type = ["administrators",
                 "controller",
                 "normalizer"]
#初始化用户对象
    def __init__(self,user_info):
        self.username = user_info["username"]
        self.prop = user_info["prop"]
        self.passwd = user_info["passwd"]

#登陆管理
class Login(object):
    #查询超级用户
    __SEARCH_SUPER_USER = f'SELECT * FROM {USER_TABLE} WHERE Prop = "administrators"'
    #计数用户
    __COUNT_USER = f'SELECT COUNT(Name) FROM {USER_TABLE} WHERE Prop = "%(prop)s"'
    #插入新用户
    __INSERT_NEW_USER = f"""REPLACE INTO {USER_TABLE}(Name,Prop,Passwd)
                                    VALUES('%(username)s','%(prop)s','%(passwd)s')
                         """
    #创建表
    __CREAT_USERTABLE = f"""CREATE TABLE IF NOT EXISTS {USER_TABLE}(
                                            Name VARCHAR(255) PRIMARY KEY,
                                            Prop VARCHAR(255),
                                            Passwd VARCHAR(512))
                        """
    #创建索引
    _CREAT_SONGTABLE_INDEX=f"CREATE INDEX IF NOT EXISTS IDXProp on {USER_TABLE}(Prop)"

    def __init__(self):
        #创建或者链接用户数据库
        self.__db = sqlite3.connect(CONFIG_DB,check_same_thread=False)

        cursor = self.__db.cursor()
        if not cursor:
            current_app.logger.error('init login db failed!')

        else:
            #创建用户表
            cursor.execute(self.__CREAT_USERTABLE)
            cursor.execute(self._CREAT_SONGTABLE_INDEX)

        cursor.close()
        self.__db.commit()

    def __del__(self):
        if not self.__db:
            self.__db.close()

    #登陆初始化
    def UserAdd(self,user):
        ret = True
        cursor = self.__db.cursor()
        #添加用户
        try:
            cursor.execute(self.__INSERT_NEW_USER % {"username":user["username"],
                                                    "prop":user["prop"],
                                                    "passwd":user["passwd"]})
        except Exception as e:
            current_app.logger.warning("Add User Failed!")
            ret = False

        cursor.close()
        self.__db.commit()
        return ret

    #是否存在超级用户
    def HasSuperUser(self):
        #查询是否存在管理员
        ret = True
        
        cursor = self.__db.cursor()
        #查询超级用户
        try:
            cursor.execute(self.__SEARCH_SUPER_USER)
            self.__db.commit()
        except Exception as e:
            print("err")

        if cursor.fetchone() == None:
            # 缺少超级用户
            ret = False
        else:
            if cursor.arraysize>1:
                # 超级用户只允许有一个
                current_app.logger.warning("Detect more than 1 super user!")
            ret = True

        cursor.close()

        return ret

#用户管理模块单元测试
if __name__ == '__main__':
    login = Login()

    #添加用户
    login.UserAdd(User({"username":"Ayden",
                        "prop":"administrators",
                        "passwd":"123456"}))
    #测试初始化
    pprint.pprint(login.HasSuperUser())





