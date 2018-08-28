# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午5:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os
import json
from multiprocessing import Pool
import beautiful_output
import datetime
import pymysql
from config import *

from tornado.options import define, options
import tornado.ioloop
import tornado.web
import os
import subprocess

define('port', default=8877, help='run on the port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        ]

        settings = dict(
            static_path='doc/site',
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
