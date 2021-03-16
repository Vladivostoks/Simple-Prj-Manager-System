# -*- coding:utf-8 -*- 
import sys
import pprint
import sqlite3
import time
import uuid

sys.path.append("..")
from config.backend_conf import AFFAIR_LIST_TABLE,ITEM_LIST_TABLE,AFFAIR_CONTENT_DATA_DB

def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d

# 单条事务具体内容数据模型:
# 1. 执行索引 INTEGER (主键)
# 2. 执行记录时间 DATETIME (索引)
# 2. 执行进展 BLOB
# 3. 执行结果 BLOB
# 4. 记录时刻的项目是否超期情况 TEXT
# 5. 当前执行项所处的项目百分比进度 INTEGER
# 6. 记录人员 TEXT
class AffairContent(object):
    # 构造
    __CREAT_AFFAIRS_CONTENT_TABLE = """CREATE TABLE IF NOT EXISTS '%(affair_id)s'(
                                       index_num        INTEGER PRIMARY KEY AUTOINCREMENT,
                                       timestamp        DATETIME NOT NULL,
                                       progress_content BLOB,
                                       progress_result  BLOB,
                                       project_status   TEXT NOT NULL,
                                       percent          INTEGER NOT NULL,
                                       author           TEXT NOT NULL);
                                    """
    # 按照时间建立索引
    __CREAT_AFFAIRS_CONTENT_INDEX = "CREATE INDEX IF NOT EXISTS IDXDate on '%(affair_id)s'(timestamp);"

    # 按照时间区间查找
    __SEARCH_CONTENT_WITH_TIME = """SELECT * FROM "%(affair_id)s"
                                    WHERE timestamp >= %(start_time)d and timestamp <= %(end_time)d
                                    ORDER BY index_num DESC;"""

    # 插入数据
    __ADD_CONTENT = """INSERT INTO '%(affair_id)s'(timestamp,progress_content,progress_result,project_status,percent,author)
                       VALUES('%(timestamp)d','%(progress_content)s','%(progress_result)s','%(project_status)s','%(percent)d','%(author)s');
                    """
    # 找到最后递增id
    __FIND_LAST_INSERT_ROWID = "SELECT LAST_INSERT_ROWID() FROM '%(affair_id)s'"
                       
    #替换数据
    __REPLACE_CONTENT = """REPLACE INTO '%(affair_id)s'(index_num,timestamp,progress_content,progress_result,project_status,percent,author)
                           VALUES('%(index)d','%(timestamp)d','%(progress_content)s','%(progress_result)s','%(project_status)s','%(percent)d','%(author)s');
                        """
    # 删除数据
    __DELETE_CONTENT = 'DELETE FROM "%(affair_id)s" WHERE index_num=%(index)d;'

    # 删除表
    __DELETE_TABLE = 'DROP TABLE "%(affair_id)s";'

    def __init__(self,db_file,affair_id):
        # 外部打开数据库后将句柄给入,按照affair_id找到表位置
        self.__affair_id = affair_id

        try:
            self.__db = sqlite3.connect(db_file)
            self.__db.row_factory = dict_factory
            cursor = self.__db.cursor()

            #为项目建表,affair_id应该是合法的
            if affair_id != "":
                cursor.execute(self.__CREAT_AFFAIRS_CONTENT_TABLE % {"affair_id":affair_id})
                cursor.execute(self.__CREAT_AFFAIRS_CONTENT_INDEX % {"affair_id":affair_id})

            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)

    def __del__(self):
        pass

    #修改一条记录
    def replace_record(self,
                       index,
                       timestamp,
                       progress_content,
                       progress_result,
                       project_status,
                       percent,
                       author):
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                cursor.execute(self.__REPLACE_CONTENT % {"affair_id":self.__affair_id,
                                                         "index":index,
                                                         "timestamp":timestamp,
                                                         "progress_content":progress_content,
                                                         "progress_result":progress_result,
                                                         "project_status":project_status,
                                                         "percent":percent,
                                                         "author":author})
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #增加/修改一条记录
    def add_record(self,
                   timestamp,
                   progress_content,
                   progress_result,
                   project_status,
                   percent,
                   author):
        try:
            cursor = self.__db.cursor()
            if self.__affair_id != "":
                cursor.execute(self.__ADD_CONTENT % {"affair_id":self.__affair_id,
                                                     "timestamp":timestamp,
                                                     "progress_content":progress_content,
                                                     "progress_result":progress_result,
                                                     "project_status":project_status,
                                                     "percent":percent,
                                                     "author":author})
                cursor.execute(self.__FIND_LAST_INSERT_ROWID % {"affair_id":self.__affair_id})
                ret = cursor.fetchone()["LAST_INSERT_ROWID()"]
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return ret

    #删除指定记录
    def delete_record(self,index):
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                cursor.execute(self.__DELETE_CONTENT % {"affair_id":self.__affair_id,
                                                        "index":index})
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #查询多条记录
    def search_record(self,start_time,end_time):
        result=[]
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                # 外部时间字符串转时间戳
                #start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d"))
                #end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d"))
                cursor.execute(self.__SEARCH_CONTENT_WITH_TIME % {"affair_id":self.__affair_id,
                                                                  "start_time":start_time,
                                                                  "end_time":end_time})
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            pprint.pprint(e)
        return result

    #查询最后一条记录
    def search_latest_record(self):
        result=[]
        try:
            cursor = self.__db.cursor()
            if self.__affair_id != "":
                # 外部时间字符串转时间戳
                #start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d"))
                #end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d"))
                # 执行记录前端输入的戳带毫秒
                cursor.execute(self.__SEARCH_CONTENT_WITH_TIME % {"affair_id":self.__affair_id,
                                                                  "start_time":0,
                                                                  "end_time":time.time()*1000})
            result = cursor.fetchone()
            cursor.close()
        except Exception as e:
            pprint.pprint(e)
        return result

    # 删除表
    def delete_table(self):
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                cursor.execute(self.__DELETE_TABLE % {"affair_id":self.__affair_id})
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

# 事务列表数据模型:
# 1. 事务uuid TEXT (主键)
# 2. 事务创建时间 DATETIME (索引)
# 3. 区域 TEXT
# 4. 事务名称 TEXT
# 5. 事务类型 TEXT
# 6. 事务描述(需求/反馈) BLOB
# 7. svn/git 代码关联路径
# 8. 事务预期时间 INTEGER
# 9. 事务执行状态 TEXT
# 10. 处理人员 TEXT
# 11. 关联人员 TEXT
# 12. 事务关联项目id(外键)
# 13. 数据最后更新时间

class AffairList(object):
## 构造
    __CREAT_AFFAIRS_LIST_TABLE = """CREATE TABLE IF NOT EXISTS %(affair_list_table)s(
                                    uuid            TEXT PRIMARY KEY,
                                    create_date      DATETIME NOT NULL,
                                    region          TEXT,
                                    prjname         TEXT NOT NULL,
                                    prjtype         TEXT NOT NULL,
                                    brief           TEXT NOT NULL,
                                    svnurl          TEXT,
                                    period          INTEGER NOT NULL,
                                    status          TEXT NOT NULL,
                                    duty_persons    TEXT NOT NULL,
                                    relate_persons  TEXT,
                                    relate_itemid   TEXT,
                                    lastupdate_date DATETIME NOT NULL)
                                """
                                    #FOREIGN KEY (relate_itemid) REFERENCES %(item_list_table)s(uuid)
                                    #ON DELETE SET NULL ON UPDATE CASCADE);
    # 按照时间建立索引
    __CREAT_AFFAIRS_LIST_INDEX = "CREATE INDEX IF NOT EXISTS IDXCreateDate on %(affair_list_table)s(create_date);"

    # 按照创建时间区间查找
    __SEARCH_AFFAIRS_WITH_TIME = """SELECT * FROM %(affair_list_table)s 
                                    WHERE create_date >= %(start_time)d and create_date <= %(end_time)d
                                 """
    # 按照更新时间去去查找
    __SEARCH_AFFAIRS_WITH_UPDATE_TIME = """SELECT * FROM %(affair_list_table)s 
                                           WHERE lastupdate_date >= %(start_time)d and lastupdate_date <= %(end_time)d
                                        """

    # 插入/替换数据
    __ADD_AFFAIRS = """REPLACE INTO %(affair_list_table)s(uuid,
                                                          create_date,
                                                          region,
                                                          prjname,
                                                          prjtype,
                                                          brief,
                                                          svnurl,
                                                          period,
                                                          status,
                                                          duty_persons,
                                                          relate_persons,
                                                          relate_itemid,
                                                          lastupdate_date)
                                                   VALUES('%(id)s',
                                                          '%(createdate)d',
                                                          '%(region)s',
                                                          '%(name)s',
                                                          '%(type)s',
                                                          '%(brief)s',
                                                          '%(svnurl)s',
                                                          '%(period)d',
                                                          '%(status)s',
                                                          '%(dutyperson)s',
                                                          '%(relateperson)s',
                                                          '%(relateitemid)s',
                                                          '%(lasteupdate_date)d');
                                                          
                    """
    # 删除数据
    __DELETE_AFFAIRS = 'DELETE FROM %(affair_list_table)s WHERE uuid="%(uuid)s"'

    def __init__(self,db_file):
        # 外部打开数据库后将句柄给入
        self.__table_name = AFFAIR_LIST_TABLE
        try:
            self.__db = sqlite3.connect(db_file)
            self.__db.row_factory = dict_factory

            cursor = self.__db.cursor()
            cursor.execute(self.__CREAT_AFFAIRS_LIST_TABLE % {"affair_list_table":self.__table_name,
                                                              "item_list_table":ITEM_LIST_TABLE})
            cursor.execute(self.__CREAT_AFFAIRS_LIST_INDEX % {"affair_list_table":self.__table_name})

            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)


    def __del__(self):
        pass
    
    #增加/修改一条记录
    def add_record(self,
                   id,
                   createdate,
                   region,
                   name,
                   type,
                   brief,
                   svnurl,
                   period,
                   status,
                   dutyperson,
                   relateperson,
                   relateitemid):
        try:
            cursor = self.__db.cursor()
            #if not createdate:
                # 直接拿时间戳
                # createdate = int(time.time())

            if not id:
                id = str(uuid.uuid4())
            
            cursor.execute(self.__ADD_AFFAIRS % {"affair_list_table":self.__table_name,
                                                 "id": id,
                                                 "createdate": createdate,
                                                 "region": region,
                                                 "name": name,
                                                 "type": ','.join(type),
                                                 "brief": brief,
                                                 "svnurl": svnurl,
                                                 "period": period,
                                                 "status": status,
                                                 "dutyperson": ','.join(dutyperson),
                                                 "relateperson": ','.join(relateperson),
                                                 "relateitemid": relateitemid,
                                                 "lasteupdate_date":int(time.time()*1000)})
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #删除指定记录
    def delete_record(self,id):
        try:
            cursor = self.__db.cursor()
            pprint.pprint(self.__DELETE_AFFAIRS % {"affair_list_table":self.__table_name,
                                                    "uuid":id})
            cursor.execute(self.__DELETE_AFFAIRS % {"affair_list_table":self.__table_name,
                                                    "uuid":id})
            cursor.close()
            self.__db.commit()
            AffairContent(AFFAIR_CONTENT_DATA_DB,id).delete_table()
        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #查询多条记录
    def search_record(self,start_time,end_time,**other_param):
        result=[]
        try:
            cursor = self.__db.cursor()

            # 时间范围为最后更新时间还是创建时间
            sql = self.__SEARCH_AFFAIRS_WITH_TIME
            if other_param["isupdatetime"] == 'true': 
                sql = self.__SEARCH_AFFAIRS_WITH_UPDATE_TIME

            if other_param["iscomplete"] == 'true': 
                sql = sql + " and (status='已完成' or status='已终止')"
            elif other_param["iscomplete"] == 'false': 
                sql = sql + " and (status='执行中' or status='暂停中')"
            else:
                pass #不限制状态

            # 是否限定人员
            if other_param["username"] and other_param["userprop"] == "normalizer": 
                # sql注入? 待测试
                sql = sql + f""" and duty_persons LIKE "{other_param['username']}" """
            cursor.execute(sql % {"affair_list_table":self.__table_name,
                                  "start_time":start_time,
                                  "end_time":end_time})
            result = cursor.fetchall()
            cursor.close()

        except Exception as e:
            pprint.pprint(e)

        # 修饰
        for res in result:
            if res["prjtype"]!=None and res["prjtype"]!="":
                res["prjtype"] = res["prjtype"].split(",")

            if res["duty_persons"]!=None and res["duty_persons"]!="":
                res["duty_persons"] = res["duty_persons"].split(",")

            if res["relate_persons"]!=None and res["relate_persons"]!="":
                res["relate_persons"] = res["relate_persons"].split(",")

        return result

#用户管理模块单元测试
if __name__ == '__main__':
    #TODO
    pass
