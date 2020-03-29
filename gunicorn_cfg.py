# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

# debug = True
loglevel = 'info'
bind = "0.0.0.0:8080"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/debug.log"
# daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
