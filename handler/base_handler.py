# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午8:36
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import tornado.web
import os


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        return self.application.db