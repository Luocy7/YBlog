# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os

import logging
from logging import FileHandler

from flask import Flask

from notes.FileObserveUtil import Watcher
from notes.filemoniter_cfg import Config
from notes.webhook import github_moniter

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask('filemoniter')
app.config.from_object(Config)

# route
app.add_url_rule('/githubwebhook', view_func=github_moniter)

# log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = FileHandler(os.path.join(basedir, 'filemonitor.log'), encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Watcher

watcher = Watcher('.')
watcher.run_with_thread()
