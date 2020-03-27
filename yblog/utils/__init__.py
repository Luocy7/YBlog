# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""
from datetime import datetime

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def str_thismonth():
    return datetime.now().strftime("%Y%m")

def str_thisday():
    return datetime.now().strftime("%Y%m%d")


def str_thishour():
    return datetime.now().strftime("%Y%m%d%H")


def str_thismin():
    return datetime.now().strftime("%Y%m%d%H%M")
