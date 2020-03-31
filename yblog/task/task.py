# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os
import time
import subprocess

from pathlib import Path

from wsgi import celery
from flask import current_app

from yblog.database.note_handle import create_post_with_file, update_post_with_file, delete_post_with_file, \
    change_post_name


@celery.task
def git_action(i):
    time.sleep(2)
    print('--!!--Job {} Done at:{}'.format(str(i).zfill(2), time.strftime('%H%M%S')))


@celery.task
def git_status():
    note_path = current_app.config['NOTE_ABS_PATH']
    cmd = current_app.config['GIT_CMD']
    os.chdir(note_path)

    ret = subprocess.run(cmd, shell=True, capture_output=True)

    if ret.returncode == 0:
        current_app.logger.info('task success\n' + ret.stdout.decode('utf-8'))
    else:
        current_app.logger.info('task fail\n' + ret.stderr.decode('utf-8'))


@celery.task
def file_created(src_path):
    src_path = Path(src_path)
    ret = create_post_with_file(src_path)
    if ret:
        current_app.logger.info('Post {} Created !'.format(src_path.stem))
    else:
        current_app.logger.error('')


@celery.task
def file_deleted(src_path):
    src_path = Path(src_path)
    ret = delete_post_with_file(src_path)
    if ret:
        current_app.logger.info('Post {} Deleted !'.format(src_path.stem))
    else:
        current_app.logger.error('')


@celery.task
def file_modified(src_path):
    src_path = Path(src_path)
    ret = update_post_with_file(src_path)
    if ret:
        current_app.logger.info('Post {} Modified !'.format(src_path.stem))
    else:
        current_app.logger.error('')


@celery.task
def file_moved(src_path, dest_path):
    src_path = Path(src_path)
    dest_path = Path(dest_path)
    ret = change_post_name(src_path, dest_path)
    if ret:
        current_app.logger.info('Post {} Renamed to {} !'.format(src_path.stem, dest_path.stem))
    else:
        current_app.logger.error('')


if __name__ == '__main__':
    git_status()
