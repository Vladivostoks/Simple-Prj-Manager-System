# -*- coding:utf-8 -*- 
import sys
import sqlite3
import pprint

from dataModel.model_version import DataModel

sys.path.append("..")
from config.backend_conf import CONFIG_DB,USER_TABLE
from dataModel.affairs_data import dict_factory

#用户数据模型:
#1. 用户名(主键)
#2. 用户属性
#3. 用户密码
class UserData(DataModel):
    #创建表
    __CREAT_USERTABLE = """CREATE TABLE IF NOT EXISTS %(user_table)s(
                           user_name VARCHAR(255) PRIMARY KEY,
                           user_prop VARCHAR(255),
                           user_passwd VARCHAR(512))
                        """
    #创建索引
    _CREAT_SONGTABLE_INDEX= "CREATE INDEX IF NOT EXISTS IDXProp on %(user_table)s(user_prop)"
    #查询:是否存在超级用户
    __SEARCH_SUPER_USER = 'SELECT * FROM %(user_table)s WHERE user_prop = "administrators"'
    #查询所有用户
    __SEARCH_ALL_USER = 'SELECT * FROM %(user_table)s'
    #查询:用户确认密码
    __CHECK_USER = 'SELECT user_prop,user_passwd FROM %(user_table)s WHERE user_name = "%(username)s"'
    #计数用户总数
    __COUNT_USER = 'SELECT COUNT(user_name) FROM %(user_table)s WHERE user_prop = "%(prop)s"'
    #插入/修改用户
    __INSERT_USER = """REPLACE INTO %(user_table)s(user_name,user_prop,user_passwd)
                                    VALUES('%(username)s','%(prop)s','%(passwd)s')
                     """
    #删除用户
    __DELETE_USER = 'DELETE FROM %(user_table)s WHERE user_name = "%(username)s"'

    #获取当前建表sql的版本号
    def get_version(self,verisons):
        verisons["user_version"] = "V1.0.0"
        return verisons

    # 外部能够访问的更新操作
    def update(self,local_verisons):
        return False,local_verisons

    def __init__(self,db_file=CONFIG_DB):
        #句柄由外部传入
        self.__table_name = USER_TABLE

        try:
            self.__db = sqlite3.connect(db_file)
            self.__db.row_factory = dict_factory

            cursor = self.__db.cursor()
            #创建用户表
            cursor.execute(self.__CREAT_USERTABLE % {"user_table":self.__table_name})
            cursor.execute(self._CREAT_SONGTABLE_INDEX % {"user_table":self.__table_name})

            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)

    def __del__(self):
        self.__db.close()

    #登陆初始化
    def user_add(self,username,prop,passwd):
        #添加用户
        try:
            cursor = self.__db.cursor()
            cursor.execute(self.__INSERT_USER % {"user_table":self.__table_name,
                                                 "username":username,
                                                 "prop":prop,
                                                 "passwd":passwd})

            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #删除用户
    def user_delete(self,username):
        #添加用户
        try:
            cursor = self.__db.cursor()
            pprint.pprint(self.__table_name)
            pprint.pprint(username)
            cursor.execute(self.__DELETE_USER % {"user_table":self.__table_name,
                                                 "username":username})

            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #用户校验
    def user_check(self,username,passwd):
        result = []
        #查询是否存在管理员
        try:
            cursor = self.__db.cursor()

            cursor.execute(self.__CHECK_USER % {"user_table":self.__table_name,
                                                "username":username})

            result = cursor.fetchone()
            cursor.close()

        except Exception as e:
            pprint.pprint(e)

        if result != None and result['user_passwd'] == '':
            #未初始化用户
            return False,result['user_prop']
        elif result == None or passwd != result['user_passwd']:
            #无此用户或密码错误
            return False,""
        else:
            return True,result['user_prop']

        return ret

    #是否存在超级用户
    def has_super_user(self):
        #查询是否存在管理员
        result = []

        #查询超级用户
        try:
            cursor = self.__db.cursor()

            cursor.execute(self.__SEARCH_SUPER_USER % {"user_table":self.__table_name})
            result = cursor.fetchall()

            cursor.close()
        except Exception as e:
            pprint.pprint(e)

        if len(result)<=0:
            # 缺少超级用户
            return False
        else:
            if len(result)>1:
                # 超级用户只允许有一个,系统异常
                print("Warning more than 1 super user!!!")

        return True

    def get_user(self,prop=None):
        #查询是否存在管理员
        result = []
        sql = self.__SEARCH_ALL_USER
        if prop:
            sql = sql + ' WHERE user_prop = ' + prop

        #查询超级用户
        try:
            cursor = self.__db.cursor()

            cursor.execute(sql % {"user_table":self.__table_name})
            result = cursor.fetchall()

            cursor.close()
        except Exception as e:
            pprint.pprint(e)

        return result

#用户管理模块单元测试
if __name__ == '__main__':
    #TODO
    pass




