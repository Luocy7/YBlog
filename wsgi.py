# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from yblog import create_app, register_celery, register_task_view

app = create_app('dev')
celery = register_celery(app)
register_task_view(app)

from yblog.utils.FileObserveUtil import Watcher

notepath = app.config['NOTE_ABS_PATH']


@app.before_first_request
def run_fileobserver():
    watcher = Watcher(notepath)
    watcher.run_with_thread()


if __name__ == '__main__':
    app.run(port=8080)
