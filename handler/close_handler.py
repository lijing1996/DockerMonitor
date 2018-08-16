# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午4:19
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class CloseHandler(BaseHandler):
    def post(self):
        cname = self.get_argument('cname')

        for node_id in range(1, 18 + 1):
            container_name = '%s.node%.2d' % (cname, node_id)
            os.system('ssh node%.2d "docker stop %s && docker rm %s"' % (node_id, container_name, container_name))

            print('close', container_name, 'done')
        self.redirect('/')
