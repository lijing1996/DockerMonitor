# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 10:06 PM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class RealGpuHandler(BaseHandler):
    def get(self):
        node_id = int(self.get_argument('id'))
        nvidia_smi_result = self.nvidia_smi(node_id)

        self.write(nvidia_smi_result)


    def nvidia_smi(self, node_id):
        node_name = 'node%.2d' % node_id
        try:
            res = os.popen("ssh %s nvidia-smi" % node_name).read()
        except:
            res = "can't access %s!" % node_name

        return res
