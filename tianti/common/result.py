#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class ResultCode(object):
    SUCCESS = 1
    FAILURE = -1


class Result(object):
    def __init__(self):
        self.code = ResultCode.FAILURE
        self.message = ""
        self.data = None

    def set_detail(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def to_json(self, ensure_ascii=True):
        json_data = {"code": self.code, "msg": self.message, "data": self.data}
        return json.dumps(json_data, ensure_ascii=ensure_ascii)

