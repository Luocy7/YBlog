# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from time import time
from datetime import datetime, timedelta
from hashlib import sha1
from urllib.parse import urlparse
from uuid import uuid4
import hmac


from flask import request, current_app

COOKIE_NAME = 'analytics'
COOKIE_DURATION = timedelta(days=1)


def _cookie_digest(payload, key=None):
    if key is None:
        key = current_app.config["SECRET_KEY"]
    payload = payload.encode("utf8")
    key = key.encode("utf8")
    mac = hmac.new(key, payload, sha1)
    return mac.hexdigest()


def _get_cookie(req):
    config = current_app.config
    cookie_name = config.get("ANALYTICS_COOKIE_NAME", COOKIE_NAME)
    request_cookie = req.headers.get('cookie', None)
    if request_cookie:
        cookies = request_cookie.split(';')
        for cookie_data in cookies:
            if cookie_name in cookie_data:
                name, value = cookie_data.split('=')
                return value
    return None


def _select_blueprint(include: list, exclude: list) -> bool:
    blprint = request.blueprint
    if include:
        return blprint in include
    elif exclude:
        return blprint not in exclude
    else:
        return True


class Analytics(object):
    analytics_callback = None

    def __init__(self, app=None):
        self.app = app
        self.cookie_value = None
        self.include = []
        self.exclude = []
        if self.app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['analytics'] = self
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def analytics_process(self, callback):
        self.analytics_callback = callback

    def before_request(self):
        if _select_blueprint(self.include, self.exclude):
            cookie_value = _get_cookie(request)
            if cookie_value:
                self.cookie_value = cookie_value
            self.track_request(request)

    def after_request(self, response):
        self._set_tracker(response)
        return response

    def _set_tracker(self, response):
        if self.cookie_value:
            return
        config = current_app.config
        name = config.get("ANALYTICS_COOKIE_NAME", COOKIE_NAME)
        domain = config.get("ANALYTICS_COOKIE_DOMAIN", None)
        duration = config.get("ANALYTICS_COOKIE_DURATION", COOKIE_DURATION)
        data = _cookie_digest(str(uuid4()))
        expires = datetime.now() + duration
        response.set_cookie(name, data, max_age=duration, expires=expires, domain=domain)

    def track_request(self, req):
        parse_result = urlparse(req.url)
        static_url_path = current_app.static_url_path
        analytics = {
            'Time': time(),
            'remote_addr': req.remote_addr,
            'cookie': self.cookie_value,
            'url': req.url,
            'blueprint': req.blueprint,
            'is_static': parse_result.path.startswith(static_url_path),
            'view_args': req.view_args,
            'platform': req.user_agent.platform,
            'browser': req.user_agent.browser,
            'browser_version': req.user_agent.version,
            'charset': req.url_charset
        }
        # save2log.delay(analytics)
        # result.wait()
        self.analytics_process(analytics)


analytis = Analytics()
analytis.analytics_process(print)
analytis.include = ['blog']
