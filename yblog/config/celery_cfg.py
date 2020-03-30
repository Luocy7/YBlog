# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""
import os

broker_url = os.environ.get('CELERY_URL', 'redis://localhost:6379/6')
result_backend = broker_url
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json', 'pickle']
include=['yblog.task.task']