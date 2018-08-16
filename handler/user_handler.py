# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午3:44
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import tornado.web
from handler.base_handler import BaseHandler
import os


class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('../html/user.html', cur_user=self.get_current_user())