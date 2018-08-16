# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午11:20
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class DiscussHandler(BaseHandler):
    def get(self):
        self.render('../html/discuss.html', cur_user=self.get_current_user())
