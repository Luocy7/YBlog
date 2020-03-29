# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/14
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from datetime import datetime
import time


class RestResponse(object):

    def __init__(self, success: bool, code: int, payload, msg):
        self.success = success
        self.code = code
        self.payload = payload
        self.msg = msg

    def format(self) -> dict:
        return {
            "success": self.success,
            "payload": self.payload,
            "msg": self.msg,
            "code": self.code,
            "timestamp": get_unixtime()
        }

    @staticmethod
    def ok(code=-1, payload=None, msg=None):
        return RestResponse(True, code, payload, msg).format()

    @staticmethod
    def fail(code=-1, payload=None, msg=None):
        return RestResponse(False, code, payload, msg).format()


def get_unixtime():
    return int(time.mktime(datetime.now().timetuple()))


if __name__ == '__main__':
    a = RestResponse.ok()
    time.sleep(3)
    b = RestResponse.fail()
    print(a)
    print(b)
