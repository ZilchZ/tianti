#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
from multiprocessing.pool import ThreadPool
from tornado.ioloop import IOLoop
from tornado.web import asynchronous
from functools import wraps
from tianti.common.logger import logger

POOL_SIZE = 25


class Async(object):
    def __init__(self):
        self.thread_pool = None

    @staticmethod
    def instance(pool_size=POOL_SIZE):
        if not hasattr(Async, "_instance"):
            with threading.Lock():
                if not hasattr(Async, "_instance"):
                    Async._instance = Async()
                    Async._instance.thread_pool = ThreadPool(pool_size)
        return Async._instance

    @staticmethod
    def async(method):
        @asynchronous
        @wraps(method)
        def wrapper(request_handler):
            def target_func():
                try:
                    method(request_handler)
                except Exception as e:
                    logger.error(e)

            def target_call_back():
                if not hasattr(request_handler, "finish"):
                    raise Exception("error asynchronous method")
                request_handler.finish()

            def callback(result):
                IOLoop.instance().add_callback(target_call_back)

            async = Async.instance()
            async.thread_pool.apply_async(target_func, (), {}, callback)

        return wrapper

    @staticmethod
    def async_scan(attr, handler_list):
        for handler in handler_list:
            if not hasattr(handler, attr):
                continue

            wrapper = Async.async(getattr(handler, attr))
            setattr(handler, attr, wrapper)
