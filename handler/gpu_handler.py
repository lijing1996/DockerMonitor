# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午4:44
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
from multiprocessing import Pool
import json
import os


def get_useful_gpu_msg(node_id):
    gpu_msg = os.popen('''ssh node%.2d '/home/piaozx/anaconda3/bin/python /home/piaozx/DockerMonitor/gpu_tools/get_gpu_msg.py' ''' % node_id).read()
    gpu_msg = json.loads(gpu_msg)
    return gpu_msg


class GpuHandler(BaseHandler):
    def get(self):
        node_gpu_msg_list = self.db.get_node_msg_list()
        self.render('../html/gpu.html', node_gpu_msg_list=node_gpu_msg_list, cur_user=self.get_current_user())


