# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午11:41
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import tornado.web
from handler.base_handler import BaseHandler
import os


class LifecycleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_lifecycle_list = self.db.get_all_user_lifecycle()

        self.render('../html/lifecycle.html', user_lifecycle_list=user_lifecycle_list, cur_user=self.get_current_user())
