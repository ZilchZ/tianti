#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options
from tianti.conf import cfg
from tianti.common.logger import logger
from tianti.handler import get_mapping, import_handlers
from tianti.handler import GET_MAPPING_DICT, POST_MAPPING_DICT, COMMON_MAPPING_DICT


@get_mapping("/index", "首页")
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.post()

    def post(self, *args, **kwargs):
        self.write("hello world")


class Launcher(object):
    def __init__(self, async=True):
        self.async = async
        self.init()

    @staticmethod
    def init():
        logger.info("--- init begin ---")
        try:
            import gc
            gc.enable()
            import_handlers()
        except Exception as e:
            logger.error(e)
        logger.info("--- init end ---")

    @staticmethod
    def async_handler(get_mapping_list, post_mapping_list):
        logger.info("--- async scan begin ---")
        from common.async import Async
        post_handler_list = [mapping[1] for mapping in post_mapping_list]
        Async.async_scan("post", post_handler_list)
        get_handler_list = [mapping[1] for mapping in get_mapping_list]
        Async.async_scan("get", get_handler_list)
        logger.info("--- async scan end ---")

    def run(self):
        logger.info("tornado server starting ... ---")
        options.define("port", default=cfg.get_config("server").get("port"), help="http server port", type=int)
        options.define("host", default=cfg.get_config("server").get("host"), help="http server host", type=int)
        settings = {
            "gzip": True,
        }
        get_mapping_list = [(r"%s" % url, GET_MAPPING_DICT[url]) for url in GET_MAPPING_DICT.keys()]
        post_mapping_list = [(r"%s" % url, POST_MAPPING_DICT[url]) for url in POST_MAPPING_DICT.keys()]
        common_mapping_list = [(r"%s" % url, COMMON_MAPPING_DICT[url]) for url in COMMON_MAPPING_DICT.keys()]
        if self.async:
            self.async_handler(get_mapping_list, post_mapping_list)
        mapping_list = get_mapping_list + post_mapping_list + common_mapping_list
        app = tornado.web.Application(mapping_list, **settings)
        server = tornado.httpserver.HTTPServer(app)
        server.listen(options.port, options.host)
        logger.info("--- tornado server run at address: %s port %s ---" % (options.host, options.port))
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.start()


if __name__ == '__main__':
    Launcher().run()
