# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/04/02
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""
from pathlib import Path

from flask import current_app

from yblog.extensions import cache
from yblog.utils.MdFileUtil import MdFile
from yblog.database.postService import *
from yblog.database.userService import get_or_create_user_by_name


def create_default_user(username, password):
    data = {
        'username': username,
        'password': password
    }
    get_or_create_user_by_name(data)


def create_default_cate():
    try:
        get_or_create_cate_by_name(catename='Default')
    except DBError as e:
        current_app.logger.error(e)


def update_posts_from_folder(folder: str):
    folder = Path(folder)
    for mdfile in folder.glob('*.md'):
        md = MdFile(str(mdfile))
        mddata = md.get_start()
        try:
            update_or_create_post_with_data(mddata)
            current_app.logger.info('Update Post <{}> Success'.format(mddata.get('md_name')))
        except DBError as e:
            current_app.logger.error(e)
    cache.clear()
