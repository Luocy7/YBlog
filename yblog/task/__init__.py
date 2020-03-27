# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/18
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import json
import time

# from yblog import redis_client as rd
# from yblog.utils import str_thishour
from yblog import celery

logfile = 'C:\\Users\\y1297\\Documents\\Project\\YBlog\\logs\\yblog.log'


@celery.task
def save2log(data: dict):
    time.sleep(2)
    with open(logfile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


@celery.task
def save2redis(data: dict):
    # rd.pfadd(str_thishour(), json.dumps(data))
    with open(logfile, 'wa', encoding='utf-8') as f:
        f.write(json.dumps(data))
