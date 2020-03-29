# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_env_value(key, default_value=''):
    return os.environ.get(key, default_value)


class YblogCfg(object):
    YBLOG_PER_PAGE = 6  # index paginate
    YBLOG_CATE_PER_PAGE = 10  # category paginate
    YBLOG_ARCHIVES_PER_PAGE = 40  # archives paginate
    YBLOG_TAG_PER_PAGE = 10  # tag paginate
    YBLOG_TOTAL_BG_COUNTS = 88  # total post cover counts
    YBLOG_SLOW_QUERY_THRESHOLD = 1
    YBLOG_AUTO_INCREMENT_VALUE = 10086


class Config(YblogCfg):
    DEBUG = False
    TESTING = False

    # Database Setting
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdljLJDL08_80jflKzcznv*c'

    REDIS_URL = os.environ.get('DEV_REDIS_URL',
                               'redis://192.168.235.129:6379/0')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                             'mysql+pymysql://luocy:luocy@192.168.235.129:3306/YBlog_dev?charset'
                                             '=utf8mb4')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'false').lower() == 'true'

    # Cache Setting
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL',
                                     'redis://192.168.235.129:6379/1')

    # Mail Server Setting
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevConfig(Config):
    DEBUG = True


class PrdConfig(Config):
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

    REDIS_URL = os.environ.get('PRD_REDIS_URL')

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRD_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
