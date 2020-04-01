# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os


class Config(object):
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ajdljLJDL08_80jflKdcznv4c'

    NOTE_ABS_PATH = os.environ.get('PRD_NOTE_PATH', 'D:\\Project\\Notable\\notes')
