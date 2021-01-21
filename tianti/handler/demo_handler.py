#!/usr/bin/python
# -*- coding: utf-8 -*-
from tianti.handler import get_mapping
from tianti.handler import BaseHandler


@get_mapping("/demo", "demo")
class Demo(BaseHandler):

    def process(self):
        return 1, "success", "demo"


@get_mapping("/demo/file", "demo file")
class DemoFile(BaseHandler):
    def __init__(self, app, request, **kwargs):
        super(DemoFile, self).__init__(app, request, **kwargs)
        self.process_type = 2

    def process(self):
        return "demo.txt", "hello world\n"