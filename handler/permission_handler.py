# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午10:47
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class PermissionHandler(BaseHandler):
    def get(self):
        user_info_list = self.db.get_all_user_info()

        self.render('../html/permission.html', user_info_list=user_info_list, cur_user=self.get_current_user())

    def post(self):
        pass
