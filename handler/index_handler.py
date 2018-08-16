# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午10:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class IndexHandler(BaseHandler):
    def get(self):
        self.render('../html/index.html', cur_user=self.get_current_user())
