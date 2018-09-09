# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午8:19
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
from config import WEBSITE_ACCOUNT_LIST


class LoginHandler(BaseHandler):
    def get(self):
        self.render("../html/login.html", cur_user=self.get_current_user())

    def post(self):
        super_username = self.get_argument('name')
        pwd = self.get_argument('pwd')

        for account in WEBSITE_ACCOUNT_LIST:
            if super_username == account['username'] and pwd == account['passwd']:
                self.set_secure_cookie("user", super_username)
                self.write('yes')
                return

        self.write('no')
