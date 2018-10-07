# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午4:19
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os
from multiprocessing import Pool


def remove_container_on_remote(node_name, container_name):
    os.system('ssh %s "docker stop %s && docker rm %s"' % (node_name, container_name, container_name))
    print('close', container_name, 'done')


class RemoveHandler(BaseHandler):
    def post(self):
        """
        code 101: blank input
        code 102: invalid input nodes
        code 103: name not exists
        code 200: success
        :return:
        """
        username = self.get_argument('cname')
        str_nodes = self.get_argument('nodes')

        ret = {'code': None}
        if username == '' or str_nodes == '':
            ret['code'] = 101
            self.write(ret)
            return

        node_list = self.get_node_list_by_str_nodes(str_nodes)
        if node_list == None:
            ret['code'] = 102
            self.write(ret)
            return

        uid = self.db.get_uid_by_username(username)
        if not uid:
            ret['code'] = 103
            self.write(ret)
            return

        p = Pool(27)
        args_list = []

        for node_id in node_list:
            node_name = 'admin' if node_id == 0 else 'node%.2d' % node_id
            container_name = '%s.%s' % (username, node_name)
            args_list.append((node_name, container_name))

        p.starmap(remove_container_on_remote, args_list)
        p.close()

        self.db.remove_user_permission(uid, node_list)
        ret['code'] = 200
        self.write(ret)
