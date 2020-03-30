# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""
import subprocess
import time

from yblog import celery


@celery.task
def git_action(i):
    time.sleep(2)
    print('--!!--Job {} Done at:{}'.format(str(i).zfill(2), time.strftime('%H%M%S')))


def git_status():
    cmd = ['git', 'status']

    subprocess.run(cmd)


if __name__ == '__main__':
    git_status()
