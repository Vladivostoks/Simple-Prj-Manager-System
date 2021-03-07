# -*- coding:utf-8 -*- 
import pprint
import sys
import threading
from flask import Flask,abort
from flask_restful import reqparse, Resource, reqparse
from dataModel import affairs_data 


sys.path.append("..")
from config.backend_conf import LIST_DATA_DB,AFFAIR_CONTENT_DATA_DB

# 用户表锁
AFFAIR_CONTENT_DATA_DB_LOCK = threading.Lock()
LIST_DATA_DB_LOCK = threading.Lock()

class AffairsContent(Resource):
    # 根据时间范围,获取当前事务列表
    def get(self, affair_id):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('start_time', dest='start_time',
                                 type=int, location='args',
                                 required=True, help='Need input start time for affair list.')
        put_parser.add_argument('end_time', dest='end_time',
                                 type=int, location='args',
                                 required=True, help='Need input end time for affair list.')
        req = put_parser.parse_args()

        AFFAIR_CONTENT_DATA_DB_LOCK.acquire()
        # 查询具体事件时间线
        ret = affairs_data.AffairContent(AFFAIR_CONTENT_DATA_DB,affair_id).search_record(**req)
        AFFAIR_CONTENT_DATA_DB_LOCK.release()

        return ret

    #删除一条事务记录
    def delete(self, affair_id):
        put_parser = reqparse.RequestParser()

        AFFAIR_CONTENT_DATA_DB_LOCK.acquire()
        put_parser.add_argument('index', dest='index',
                                type=int, location='json',
                                required=True, help='Need input index for delete from affair content.')
        req = put_parser.parse_args()
        # 查询具体事件时间线
        ret = affairs_data.AffairContent(AFFAIR_CONTENT_DATA_DB,affair_id).delete_record(**req)
        AFFAIR_CONTENT_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"删除失败"}', 200
        else:
            return '{"message":"删除成功"}', 200
    
    #完成事务的修改和添加
    def put(self, affair_id):
        put_parser = reqparse.RequestParser()

        # 插入具体事件时间线
        put_parser.add_argument('index', dest='index',
                                type=int, location='json',
                                required=False)
        put_parser.add_argument('date', dest='date',
                                type=int, location='json',
                                required=True, help='Need input region for creating affair.')
        put_parser.add_argument('progress_content', dest='progress_content',
                                type=str, location='json',
                                required=True, help='Need input affair name for creating affair.')
        put_parser.add_argument('progress_result', dest='progress_result',
                                type=str, location='json',
                                required=True, help='Need input affair type for creating affair.')
        put_parser.add_argument('percent', dest='percent',
                                type=int, location='json',
                                required=True, help='Need input brief for creating affair.')
        req = put_parser.parse_args()

        AFFAIR_CONTENT_DATA_DB_LOCK.acquire()
        if req["index"]:
            ret = affairs_data.AffairContent(AFFAIR_CONTENT_DATA_DB,affair_id).replace_record(**req)
        else:
            req.pop("index")
            ret = affairs_data.AffairContent(AFFAIR_CONTENT_DATA_DB,affair_id).add_record(**req)
        AFFAIR_CONTENT_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"插入失败"}', 200
        else:
            return '{"message":"插入成功"}', 200


class Affairs(Resource):
    # 根据时间范围,获取当前事务列表
    def get(self):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('start_time', dest='start_time',
                                 type=str, location='args',
                                 required=True, help='Need input start time for affair list.')
        put_parser.add_argument('end_time', dest='end_time',
                                 type=str, location='args',
                                 required=True, help='Need input end time for affair list.')
        put_parser.add_argument('iscomplete', dest='iscomplete',
                                 type=str, location='args',
                                 required=False)
        put_parser.add_argument('isupdatetime', dest='isupdatetime',
                                 type=str, location='args',
                                 required=False)
        put_parser.add_argument('userprop', dest='userprop',
                                 type=str, location='args',
                                 required=False)
        put_parser.add_argument('username', dest='username',
                                 type=str, location='args',
                                 required=False)
        req = put_parser.parse_args()

        LIST_DATA_DB_LOCK.acquire()
        # 查询事件列表
        ret = affairs_data.AffairList(LIST_DATA_DB).search_record(**req)
        LIST_DATA_DB_LOCK.release()

        return ret

    #删除一条事务记录
    def delete(self):
        put_parser = reqparse.RequestParser()

        LIST_DATA_DB_LOCK.acquire()
        put_parser.add_argument('uuid', dest='id',
                                type=str, location='json',
                                required=True, help='Need input uuid for delete from affair list.')
        req = put_parser.parse_args()
        # 查询事件列表
        ret = affairs_data.AffairList(LIST_DATA_DB).delete_record(**req)
        LIST_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"删除失败"}', 200
        else:
            return '{"message":"删除成功"}', 200
    
    #完成事务的修改和添加
    def put(self):
        put_parser = reqparse.RequestParser()
        # 插入单个事件列表
        put_parser.add_argument('uuid', dest='id', #action='append',
                                type=str, location='json',
                                required=False)
        put_parser.add_argument('create_date', dest='createdate',
                                type=str, location='json',
                                required=False)
        put_parser.add_argument('region', dest='region',
                                type=str, location='json',
                                required=True, help='Need input region for creating affair.')
        put_parser.add_argument('prjname', dest='name',
                                type=str, location='json',
                                required=True, help='Need input affair name for creating affair.')
        put_parser.add_argument('prjtype', dest='type',
                                type=list, location='json',
                                required=True, help='Need input affair type for creating affair.')
        put_parser.add_argument('brief', dest='brief',
                                type=str, location='json',
                                required=True, help='Need input brief for creating affair.')
        put_parser.add_argument('svnurl', dest='svnurl',
                                type=str, location='json',
                                required=False)
        put_parser.add_argument('period', dest='period',
                                type=int, location='json',
                                required=True, help='Need input period for creating affair.')
        put_parser.add_argument('status', dest='status',
                                type=str, location='json',
                                required=True, help='Need input status for creating affair.')
        put_parser.add_argument('duty_persons', dest='dutyperson',
                                type=list, location='json',
                                required=True, help='Need input dutyperson for creating affair.')
        put_parser.add_argument('relate_persons', dest='relateperson',
                                type=list, location='json',
                                required=False)
        put_parser.add_argument('relate_itemid', dest='relateitemid',
                                type=str, location='json',
                                required=False)
        req = put_parser.parse_args()
        LIST_DATA_DB_LOCK.acquire()
        ret = affairs_data.AffairList(LIST_DATA_DB).add_record(**req)
        LIST_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"插入失败"}', 200
        else:
            return '{"message":"插入成功"}', 200
