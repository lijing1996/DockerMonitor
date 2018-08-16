# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午7:10
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import tornado.web
from handler.base_handler import BaseHandler
import os


class SystemHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('../html/system.html', cur_user=self.get_current_user())
