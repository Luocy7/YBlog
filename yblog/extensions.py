# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect

toolbar = DebugToolbarExtension()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
md = Misaka(fenced_code=True, autolink=True, highlight=True, math=True)
cache = Cache()


@login_manager.user_loader
def load_user(user_id):
    from yblog.database.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_message_category = 'warning'
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录后访问该页面'
