# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_redis import FlaskRedis
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
moment = Moment()
toolbar = DebugToolbarExtension()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
md = Misaka(fenced_code=True, autolink=True, highlight=True, math=True)
redis_client = FlaskRedis()
cache = Cache()


@login_manager.user_loader
def load_user(user_id):
    from yblog.common.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_message_category = 'warning'
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录后访问该页面'
