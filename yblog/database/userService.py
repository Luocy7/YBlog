# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/31
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from yblog import db
from yblog.database.models import Admin


def get_or_create_user_by_name(data: dict):
    _admin = Admin.query.filter(Admin.user_name == data.get('username')).first()
    if not _admin:
        admin = Admin()
        admin.user_name = data.get('username', 'Luocy')
        admin.password = data.get('password', 'Luocy')
        admin.email = data.get('email', '')
        admin.avatar = data.get('avatar', '')
        db.session.add(admin)
        db.session.commit()
    return _admin


def update_user_with_data(data: dict):
    admin = get_or_create_user_by_name(data)
    admin.email = data.get('email', '')
    admin.password = data.get('password', 'Luocy')
    admin.avatar = data.get('avatar', '')
    db.session.add(admin)
    db.session.commit()