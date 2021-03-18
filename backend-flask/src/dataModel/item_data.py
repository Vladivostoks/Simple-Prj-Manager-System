# -*- coding:utf-8 -*- 
from pprint import pprint
import datetime
import uuid

# 具体项目数据模型:
# 1. 项目标记点
# 1. 项目标记点





# 项目列表数据模型:
# 1. 项目uuid TEXT (主键)
# 2. 项目创建时间 DATETIME (索引)
# 4. 项目名称 TEXT
# 6. 项目简介 BLOB
# 9. 参与人员 TEXT
# 3. 区域 TEXT
# 7. 项目预计到期时间 DATETIME
class ItemList(object):
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

        try:
            cursor = self.__db.cursor()

            #为项目建表,affair_id应该是合法的
            if affair_id != "":
                cursor.execute(self.__CREAT_AFFAIRS_LIST_TABLE % {"affair_list_table":table_name})
                cursor.execute(self.__CREAT_AFFAIRS_LIST_INDEX % {"affair_list_table":table_name})
        except Exception as e:
            pprint(e)

        cursor.close()
        self.__db.commit()

    def __del__(self):
        self.__db.close()

    #增加/修改一条记录
    def add_record(self,
                   createdate,
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

            today_time = str(datetime.datetime.now()).split('.')[0]
            print(today_time)
            today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')

            cursor.execute(self.__ADD_AFFAIRS % {"id": str(uuid.uuid4()),
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
        except Exception as e:
            pprint(e)
            return False

        cursor.close()
        self.__db.commit()
        return True

    #删除指定记录
    def delete_record(self,index):
        try:
            cursor = self.__db.cursor()

            if self.__affair_id != "":
                cursor.execute(self.__ADD_CONTENT % {"affair_id":self.__affair_id,
                                                     "index":index})
        except Exception as e:
            pprint(e)
            return False

        cursor.close()
        self.__db.commit()
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
        except Exception as e:
            pprint(e)

        result = cursor.fetchall()
        cursor.close()

        return result
#用户管理模块单元测试
if __name__ == '__main__':
    #TODO
    pass
