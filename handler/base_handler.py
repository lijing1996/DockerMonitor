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

    def get_uid_by_uname(self, cname):
        if cname == "":
            return None

        uid = os.popen("grep %s /etc/passwd | cut -f3 -d':'" % cname).read().strip()
        if uid != "":
            return int(uid)
        else:
            return None

    def get_node_list_by_str_nodes(self, nodes):
        try:
            node_list = eval('[%s]' % nodes)
        except:
            return None

        if not isinstance(node_list, list) or len(node_list) == 0:
            return None

        standard_node_list = list(range(1, 18 + 1))
        for node_id in node_list:
            if node_id not in standard_node_list:
                return None
        return node_list
