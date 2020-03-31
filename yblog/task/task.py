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
    command = current_app.config['GIT_CMD']
    cmd = command.split(' ') if command else ['cd', '&&git', 'status']

    ret = subprocess.run(cmd, shell=True, capture_output=True)

    if ret.returncode == 0:
        current_app.logger.info('task success\n'+ret.stdout.decode('utf-8'))
    else:
        current_app.logger.info('task fail\n'+ret.stderr.decode('utf-8'))


if __name__ == '__main__':
    git_status()
