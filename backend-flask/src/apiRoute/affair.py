# -*- coding:utf-8 -*- 
from flask_restful import reqparse, Resource



class Affairs(Resource):
    #根据时间范围,获取当前事务列表
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    #删除一条事务记录
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204
    
    #完成事务的修改和添加
    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201
