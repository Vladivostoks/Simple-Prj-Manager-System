# -*- coding:utf-8 -*- 
import sqlite3
import pprint

#用户数据模型:
#1. 用户名(主键)
#2. 用户属性
#3. 用户密码
class User(object):
    #创建表
    __CREAT_USERTABLE = """CREATE TABLE IF NOT EXISTS %(user_table)s(
                           Name VARCHAR(255) PRIMARY KEY,
                           Prop VARCHAR(255),
                           Passwd VARCHAR(512))
                        """
    #创建索引
    _CREAT_SONGTABLE_INDEX= "CREATE INDEX IF NOT EXISTS IDXProp on %(user_table)s(Prop)"
    #查询:是否存在超级用户
    __SEARCH_SUPER_USER = 'SELECT * FROM %(user_table)s WHERE Prop = "administrators"'
    #查询:用户确认密码
    __CHECK_USER = 'SELECT Prop,Passwd FROM %(user_table)s WHERE Name = "%(username)s"'
    #计数用户总数
    __COUNT_USER = 'SELECT COUNT(Name) FROM %(user_table)s WHERE Prop = "%(prop)s"'
    #插入/修改用户
    __INSERT_USER = """REPLACE INTO %(user_table)s(Name,Prop,Passwd)
                                    VALUES('%(username)s','%(prop)s','%(passwd)s')
                     """
    #删除用户
    __DELETE_USER = 'DELETE FROM %(user_table)s WHERE Name = "%(username)s"'

    def __init__(self,db_file,table_name):
        #句柄由外部传入
        self.__table_name = table_name

        try:
            self.__db = sqlite3.connect(db_file)

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

        if result != None and result[1] == None:
            #未初始化用户
            return True,""
        elif result == None or passwd != result[1]:
            #无此用户或密码错误
            return False,""
        else:
            return True,result[0]

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

        pprint.pprint(result)
        if len(result)<=0:
            # 缺少超级用户
            return False
        else:
            if len(result)>1:
                # 超级用户只允许有一个,系统异常
                print("Warning more than 1 super user!!!")

        return True

#用户管理模块单元测试
if __name__ == '__main__':
    #TODO
    pass




