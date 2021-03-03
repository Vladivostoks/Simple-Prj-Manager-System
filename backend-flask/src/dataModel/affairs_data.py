# -*- coding:utf-8 -*- 
import pprint
import sqlite3
import datetime
import uuid

# 单条事务具体内容数据模型:
# 1. 执行索引 INTEGER (主键)
# 2. 执行记录时间 DATETIME (索引)
# 2. 执行进展 BLOB
# 3. 执行结果 BLOB
# 4. 当前执行项所处的项目百分比进度 INTEGER
class AffairContent(object):
    # 构造
    __CREAT_AFFAIRS_CONTENT_TABLE = """CREATE TABLE IF NOT EXISTS %(affair_id)s(
                                       Index           INTEGER PRIMARY KEY AUTOINCREMENT,
                                       Date            DATETIME NOT NULL,
                                       ProgressContent BLOB,
                                       ProgressResult  BLOB,
                                       Percent         INTEGER NOT NULL);
                                    """
    # 按照时间建立索引
    __CREAT_AFFAIRS_CONTENT_INDEX = "CREATE INDEX IF NOT EXISTS IDXDate on %(affair_id)s(Date);"

    # 按照时间区间查找
    __SEARCH_CONTENT_WITH_TIME = """SELECT * FROM %(affair_id)s 
                                    WHERE Date >= %(start_time)d and Date <= %(end_time)d
                                    ORDER BY Date,Percent DESC;"""

    # 插入数据
    __ADD_CONTENT = """REPLACE INTO %(affair_id)s(Date,ProgressContent,ProgressResult,Percent)
                       VALUES('%(date)d','%(progress_content)s','%(progress_result)s','%(percent)d');
                    """
    # 删除数据
    __DELETE_CONTENT = 'DELETE FROM %(affair_id)s WHERE Index=%(index)d'

    def __init__(self,db,affair_id):
        # 外部打开数据库后将句柄给入,按照affair_id找到表位置
        self.__db = db
        self.__affair_id = affair_id

        try:
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

    #增加/修改一条记录
    def add_record(self,
                   index=-1,
                   date,
                   progress_content,
                   progress_result,
                   percent):
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                cursor.execute(self.__ADD_CONTENT % {"affair_id":self.__affair_id,
                                                     "date":date,
                                                     "progress_content":progress_content,
                                                     "progress_result":progress_result,
                                                     "percent":percent})
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

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
                cursor.execute(self.__SEARCH_CONTENT_WITH_TIME % {"affair_id":self.__affair_id,
                                                                  "start_time":start_time,
                                                                  "end_time":end_time})
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            pprint.pprint(e)

        return result

# 事务列表数据模型:
# 1. 事务uuid TEXT (主键)
# 2. 事务创建时间 DATETIME (索引)
# 3. 区域 TEXT
# 4. 事务名称 TEXT
# 5. 事务类型 TEXT
# 6. 事务描述(需求/反馈) BLOB
# 7. 事务预期时间 INTEGER
# 8. 事务执行状态 TEXT
# 9. 处理人员 TEXT
# 10. 关联人员 TEXT
# 11. 事务关联项目id(外键)
class AffairList(object):
## 构造
    __CREAT_AFFAIRS_LIST_TABLE = """CREATE TABLE IF NOT EXISTS %(affair_list_table)s(
                                    ID           TEXT PRIMARY KEY,
                                    CreateDate   DATETIME NOT NULL,
                                    Region       TEXT,
                                    Name         TEXT NOT NULL,
                                    Type         TEXT NOT NULL,
                                    Brief        TEXT NOT NULL,
                                    Period       INTEGER NOT NULL,
                                    Status       TEXT NOT NULL,
                                    DutyPerson   TEXT NOT NULL,
                                    RelatePerson TEXT,
                                    RelateItemId TEXT,
                                    FOREIGN KEY (RelateItemId) REFERENCES %(item_list_table)s(ID)
                                    ON DELETE SET NULL ON UPDATE CASCADE);
                                """
    # 按照时间建立索引
    __CREAT_AFFAIRS_LIST_INDEX = "CREATE INDEX IF NOT EXISTS IDXCreateDate on %(affair_list_table)s(CreateDate);"

    # 按照时间区间查找
    __SEARCH_AFFAIRS_WITH_TIME = """SELECT * FROM %(affair_list_table)s 
                                    WHERE CreateDate >= %(start_time)d and CreateDate <= %(end_time)d;
                                 """

    # 插入数据
    __ADD_AFFAIRS = """REPLACE INTO %(affair_list_table)s(ID,
                                                          CreateDate,
                                                          Region,
                                                          Name,
                                                          Type,
                                                          Brief,
                                                          Period,
                                                          Status,
                                                          DutyPerson,
                                                          RelatePerson,
                                                          RelateItemId)
                                                   VALUES('%(id)s',
                                                          '%(createdate)d',
                                                          '%(region)s',
                                                          '%(name)s',
                                                          '%(type)s',
                                                          '%(brief)s',
                                                          '%(period)d',
                                                          '%(status)s',
                                                          '%(dutyperson)s',
                                                          '%(relateperson)s',
                                                          '%(relateitemid)s');
                    """
    # 删除数据
    __DELETE_AFFAIRS = 'DELETE FROM %(affair_list_table)s WHERE ID=%(uuid)s'

    def __init__(self,db,table_name):
        # 外部打开数据库后将句柄给入
        self.__db = db
        self.__table_name = table_name
        try:
            cursor = self.__db.cursor()

            #为项目建表,affair_id应该是合法的
            if affair_id != "":
                cursor.execute(self.__CREAT_AFFAIRS_LIST_TABLE % {"affair_list_table":self.__table_name})
                cursor.execute(self.__CREAT_AFFAIRS_LIST_INDEX % {"affair_list_table":self.__table_name})

            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)


    def __del__(self):
        pass
    
    #增加/修改一条记录
    def add_record(self,
                   createdate=0,
                   region,
                   name,
                   type,
                   brief,
                   period,
                   status,
                   dutyperson,
                   relateperson,
                   relateitemid):
        try:
            cursor = self.__db.cursor()

            if createdate==0:
                today_time = str(datetime.datetime.now()).split('.')[0]
                createdate = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')

            cursor.execute(self.__ADD_AFFAIRS % {"affair_list_table":self.__table_name,
                                                 "id": str(uuid.uuid4()),
                                                 "createdate": createdate,
                                                 "region": region,
                                                 "name": name,
                                                 "type": type,
                                                 "brief": brief,
                                                 "period": period,
                                                 "status": status,
                                                 "dutyperson": dutyperson,
                                                 "relateperson": relateperson,
                                                 "relateitemid": relateitemid})
            cursor.close()
            self.__db.commit()

        except Exception as e:
            pprint.pprint(e)
            return False

        return True

    #删除指定记录
    def delete_record(self,uuid):
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                cursor.execute(self.__DELETE_AFFAIRS % {"affair_list_table":self.__table_name,
                                                        "uuid":uuid})
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
            cursor.execute(self.__SEARCH_AFFAIRS_WITH_TIME % {"affair_list_table":self.__table_name,
                                                                "start_time":start_time,
                                                                "end_time":end_time})
            result = cursor.fetchall()
            cursor.close()

        except Exception as e:
            pprint.pprint(e)


        return result

#用户管理模块单元测试
if __name__ == '__main__':
    #TODO
    pass
