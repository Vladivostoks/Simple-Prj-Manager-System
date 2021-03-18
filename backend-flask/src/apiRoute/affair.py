# -*- coding:utf-8 -*- 
import pprint
import sys
import threading
import time
from flask import Flask,abort
from flask_restful import reqparse, Resource, reqparse
from dataModel import affairs_data 


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
        ret = affairs_data.AffairContent(affair_id).search_record(**req)
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
        ret = affairs_data.AffairContent(affair_id).delete_record(**req)
        AFFAIR_CONTENT_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"删除失败"}', 200
        else:
            return '{"message":"删除成功"}', 200
    
    #完成事务的修改和添加
    def post(self, affair_id):
        put_parser = reqparse.RequestParser()

        # 插入具体事件时间线
        put_parser.add_argument('index', dest='index',
                                type=int, location='json',
                                required=False)
        put_parser.add_argument('timestamp', dest='timestamp',
                                type=int, location='json',
                                required=True, help='Need input date or type error.')
        put_parser.add_argument('progress_content', dest='progress_content',
                                type=str, location='json',
                                required=True, help='Need input progress_content or type error.')
        put_parser.add_argument('progress_result', dest='progress_result',
                                type=str, location='json',
                                required=True, help='Need input progress_result or type error.')
        put_parser.add_argument('project_status', dest='project_status',
                                type=str, location='json',
                                required=True, help='Need input project_status or type error.')
        put_parser.add_argument('percent', dest='percent',
                                type=int, location='json',
                                required=True, help='Need input percent or type error.')
        put_parser.add_argument('author', dest='author',
                                type=str, location='json',
                                required=True, help='Need input author or type error.')
        req = put_parser.parse_args()

        AFFAIR_CONTENT_DATA_DB_LOCK.acquire()
        if req["index"]:
            ret = affairs_data.AffairContent(affair_id).replace_record(**req)
        else:
            req.pop("index")
            ret = affairs_data.AffairContent(affair_id).add_record(**req)
        AFFAIR_CONTENT_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"插入失败"}', 200
        else:
            return f'{{"message":"插入成功","index_num":{ret}}}', 200


class Affairs(Resource):
    # 根据时间范围,获取当前事务列表
    def get(self):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument('start_time', dest='start_time',
                                 type=int, location='args',
                                 required=True, help='Need input start time for affair list.')
        put_parser.add_argument('end_time', dest='end_time',
                                 type=int, location='args',
                                 required=True, help='Need input end time for affair list.')
        put_parser.add_argument('iscomplete', dest='iscomplete',
                                 type=str, location='args',
                                 required=False)
        put_parser.add_argument('isupdatetime', dest='isupdatetime',
                                 type=str, location='args',
                                 required=False)
        put_parser.add_argument('userprop', dest='userprop',
                                 type=str, location='cookies',
                                 required=False)
        put_parser.add_argument('username', dest='username',
                                 type=str, location='cookies',
                                 required=False)
        req = put_parser.parse_args()

        LIST_DATA_DB_LOCK.acquire()
        # 查询事件列表
        ret = affairs_data.AffairList().search_record(**req)
        LIST_DATA_DB_LOCK.release()

        # 查询具体事务,调整部分事件列表中的内容
        for affair in ret:
            AFFAIR_CONTENT_DATA_DB_LOCK.acquire()
            # 查询具体事件时间线
            timeline = affairs_data.AffairContent(affair["uuid"]).search_latest_record()
            AFFAIR_CONTENT_DATA_DB_LOCK.release()

            if timeline:
                if (time.time()*1000-timeline["timestamp"]) > 7*24*60*60*1000:
                    if affair["status"]=="执行中":
                        # 超过一周没更新，执行任务状态设置为暂停
                        affair["status"] = "暂停中" 
                else:
                    if affair["status"]!="已完成" and affair["status"]!="已终止":
                        # 超过一周没更新，执行任务状态设置为暂停
                        affair["status"] = "执行中" 
                        affair["percent"] = timeline['percent']
                    else:
                        affair["percent"] = 100
            else:
                if (time.time()-affair["create_date"]) > 7*24*60*60 and affair["status"]=="执行中":
                    affair["status"] = "暂停中" 
                affair["percent"] = 0
            #affair["create_date"] = time.strftime("%Y-%m-%d", time.localtime(affair["create_date"]))

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
        ret = affairs_data.AffairList().delete_record(**req)
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
                                type=int, location='json',
                                required=True, help='Need input region for creating timestamp.')
        put_parser.add_argument('region', dest='region',
                                type=str, location='json',
                                required=True, help='Need input region for creating affair.')
        put_parser.add_argument('prjname', dest='name',
                                type=str, location='json',
                                required=True, help='Need input affair name for creating affair.')
        put_parser.add_argument('prjtype', dest='type',
                                type=list, location='json',
                                required=True, help='Need input affair type for creating affair.')
        put_parser.add_argument('prjmodel', dest='model',
                                type=list, location='json',
                                required=False)
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
        ret = affairs_data.AffairList().add_record(**req)
        LIST_DATA_DB_LOCK.release()

        if not ret:
            return '{"message":"插入失败"}', 200
        else:
            return '{"message":"插入成功"}', 200
