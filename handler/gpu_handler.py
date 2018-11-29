# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午4:44
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler

class GpuHandler(BaseHandler):
    def get(self):
        node_id = int(self.get_argument('id', default=-1))
        if node_id == -1:
            node_gpu_msg_list = self.db.get_node_msg_list()
            self.render('../html/gpu.html', node_gpu_msg_list=node_gpu_msg_list, cur_user=self.get_current_user())
        else:
            node_gpu_msg_list = self.db.get_node_msg_list()
            self.write(json.dumps(node_gpu_msg_list))


class P40GpuHandler(BaseHandler):
    def get(self):
        node_id = int(self.get_argument('id', default=-1))
        if node_id == -1:
            node_gpu_msg_list = self.db.get_p40_node_msg_list()
            self.render('../html/p40_gpu.html', node_gpu_msg_list=node_gpu_msg_list, cur_user=self.get_current_user())
        else:
            node_gpu_msg_list = self.db.get_p40_node_msg_list()
            self.write(json.dumps(node_gpu_msg_list))
#         node_gpu_msg_list = self.db.get_p40_node_msg_list()
#         self.render('../html/p40_gpu.html', node_gpu_msg_list=node_gpu_msg_list, cur_user=self.get_current_user())

class CoursesGpuHandler(BaseHandler):
    def get(self):
        node_gpu_msg_list = self.db.get_courses_node_msg_list()
        self.render('../html/courses_gpu.html', node_gpu_msg_list=node_gpu_msg_list, cur_user=self.get_current_user())
