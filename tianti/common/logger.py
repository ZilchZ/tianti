#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import tornado.log
from tianti.conf import cfg
from tianti.util.singleton import singleton


@singleton
class Logger(object):

    def __init__(self):
        logging.basicConfig(
            format="[%(asctime)s][%(thread)d %(threadName)s][%(filename)s][%(pathname)s:%(lineno)d][%(levelname)s] - %(message)s"
        )
        self.logger = logging.getLogger()
        fmt = tornado.log.LogFormatter(
            fmt="[%(asctime)s][%(thread)d %(threadName)s][%(filename)s][%(pathname)s:%(lineno)d][%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        tornado.log.enable_pretty_logging(logger=self.logger)


        if cfg.get_config("log").get("debug").lower() == "true":
            self.logger.setLevel(logging.DEBUG)
        self.logger.handlers[0].setFormatter(fmt)

    def get_logger(self):
        return self.logger


logger = Logger()
logger = logger.get_logger()


if __name__ == '__main__':
    logger.info("info xxx")
    logger.error("error xxx")

