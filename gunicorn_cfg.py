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
accesslog = "-"
errorlog = "-"

access_log_format = '%({x-forwarded-for}i)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
# daemon = True

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
