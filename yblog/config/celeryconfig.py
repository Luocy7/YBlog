# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

broker_url = 'redis://192.168.235.129:6379/0'
result_backend = 'redis://192.168.235.129:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json', 'pickle']
include=['yblog.task']
