# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午4:19
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class RemoveHandler(BaseHandler):
    def post(self):
        """
        code 101: name not exists
        code 102: wrong nodes or not exists
        code 200: ok
        :return:
        """
        cname = self.get_argument('cname')
        ret = {}

        for node_id in range(1, 18 + 1):
            container_name = '%s.node%.2d' % (cname, node_id)
            os.system('ssh node%.2d "docker stop %s && docker rm %s"' % (node_id, container_name, container_name))

            print('close', container_name, 'done')
        self.redirect('/')

