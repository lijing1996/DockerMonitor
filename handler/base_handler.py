# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午8:36
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import tornado.web
import os

STANDARD_NODE_LIST = list(range(0, 35 + 1))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        return self.application.db

    def get_node_list_by_str_nodes(self, nodes):
        try:
            node_list = eval('[%s]' % nodes)
        except:
            return None

        if not isinstance(node_list, list) or len(node_list) == 0:
            return None

        for node_id in node_list:
            if node_id not in STANDARD_NODE_LIST:
                return None
        return node_list
