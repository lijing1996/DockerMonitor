# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午8:19
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
from config import WEBSITE_USERNAME, WEBSITE_PASSWORD


class LoginHandler(BaseHandler):
    def get(self):
        self.render("../html/login.html", cur_user=self.get_current_user())

    def post(self):
        super_username = self.get_argument('name')
        pwd = self.get_argument('pwd')

        if super_username == WEBSITE_USERNAME and pwd == WEBSITE_PASSWORD:
            self.set_secure_cookie("user", super_username)
            self.write('yes')
        else:
            self.write('no')
