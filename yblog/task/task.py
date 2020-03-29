# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import time

from yblog import celery


@celery.task
def git_action():
    time.sleep(3)
    print('123')
