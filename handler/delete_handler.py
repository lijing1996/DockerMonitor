# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午10:00
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os


class DeleteHandler(BaseHandler):
    def post(self):
        '''
        code 101: blank input
        code 102: name not exists
        code 200: success
        :return:
        '''
        cname = self.get_argument('cname')

        ret = {'code': None}
        if cname == "":
            ret['code'] = 101
            self.write(ret)
            return

        uid = self.db.get_uid_by_username(cname)
        if uid == None:
            ret['code'] = 102
            self.write(ret)
            return

        self.close_all_container(cname, uid)

        print('rm -rf /public/docker/%s...' % cname)
        os.system('rm -rf /public/docker/%s' % cname)
        print('delete account successfully!!!')

        self.db.delete_user(uid)
        ret['code'] = 200
        self.write(ret)

    def close_all_container(self, cname, uid):
        node_list = list(range(1, 18 + 1))

        for node_id in node_list:
            container_name = '%s.node%.2d' % (cname, node_id)
            os.system('ssh node%.2d "docker stop %s && docker rm %s"' % (node_id, container_name, container_name))

            print('close', container_name, 'done')

        container_name = '%s.admin' % cname
        os.system('docker stop %s && docker rm %s' % (container_name, container_name))
        print('close', container_name, 'done')

        self.db.remove_user_permission(uid, [0] + node_list)
