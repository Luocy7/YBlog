# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""
import subprocess
import time

from wsgi import celery
from flask import current_app


@celery.task
def git_action(i):
    time.sleep(2)
    print('--!!--Job {} Done at:{}'.format(str(i).zfill(2), time.strftime('%H%M%S')))


@celery.task
def git_status():
    cmd = ['cd', 'notes\\input', '&&cd', '&&git', 'status']

    ret = subprocess.run(cmd, shell=True, capture_output=True)

    print(ret.stdout.decode('utf-8'))

    if ret.returncode == 0:
        print('task success')
        current_app.logger.info(ret.stdout.decode('utf-8'))
    else:
        print('task fail')


if __name__ == '__main__':
    git_status()
