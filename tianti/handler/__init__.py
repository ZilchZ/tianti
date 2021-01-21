#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from tianti.common.result import Result
from tianti.common.logger import logger
from tornado.web import RequestHandler

POST_MAPPING_DICT = {}
GET_MAPPING_DICT = {}
COMMON_MAPPING_DICT = {}
URI_NAME_MAPPING_DICT = {}


class BaseHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.process_type = 1 # 1 处理json 2 处理file

    def get(self, *args, **kwargs):
        self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.process_type == 1:
            result = Result()
            status, message, data = None, None, None
            try:
                logger.info("entry: %s" % self.request.path)
                status, message, data = self.process()
                if status != 1:
                    self.set_status(500)
                result.set_detail(status, message, data)
            except Exception as e:
                self.set_status(500)
                result.set_detail(
                    status if status is not None else -1,
                    message if message is not None else str(e),
                    data
                )
                logger.error(e)
            self.write_result(result)
        elif self.process_type == 2:
            file_name, data = self.process()
            self.write_file(data, file_name)
        else:
            self.write_result(Result())

    def write_file(self, result, filename):
        try:
            self.set_header("Content-Type", "application/octet-stream")
            self.set_header("Content-Disposition", "attachment;filename=" + filename)
            self.write(result)
            self.flush()
        except Exception as e:
            logger.error(e)

    def write_result(self, result):
        try:
            self.set_header("Content-Type", "application/json")
            self.write(result.to_json())
        except Exception as e:
            logger.error(e)

    def process(self):
        raise Exception("not implement!")


def post_mapping(url, url_name):
    def wrap(cls):
        if POST_MAPPING_DICT.get(url):
            raise Exception("url path:%s is exists" % url)
        POST_MAPPING_DICT[url] = cls
        if URI_NAME_MAPPING_DICT.get(url):
            raise Exception("url path:%s is exists" % url)
        URI_NAME_MAPPING_DICT[url] = url_name
        return cls

    return wrap


def get_mapping(url, url_name):
    def wrap(cls):
        if GET_MAPPING_DICT.get(url):
            raise Exception("url path:%s is exists" % url)
        GET_MAPPING_DICT[url] = cls
        if URI_NAME_MAPPING_DICT.get(url):
            raise Exception("url path:%s is exists" % url)
        URI_NAME_MAPPING_DICT[url] = url_name
        return cls

    return wrap


def common_mapping(url, url_name):
    def wrap(cls):
        if COMMON_MAPPING_DICT.get(url):
            raise Exception("url path:%s is exists" % url)
        POST_MAPPING_DICT[url] = cls
        if URI_NAME_MAPPING_DICT.get(url):
            raise Exception("url path:%s is exists" % url)
        URI_NAME_MAPPING_DICT[url] = url_name
        return cls

    return wrap


def get_cur_dif_files():
    modules = []
    dir = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(dir):
        f_tuple = os.path.splitext(f)
        if f_tuple[-1] == ".py":
            modules.append(f_tuple[0])
    return modules


def import_handlers():
    prefix_path = "tianti.handler"
    modules = get_cur_dif_files()
    for module in set(modules):
        try:
            __import__("%s.%s" % (prefix_path, module))
        except Exception as e:
            logger.info("import package failed. module=%s [%s]" % (module, e))
