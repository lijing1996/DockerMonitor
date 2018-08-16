# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午10:00
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os

class DeleteHandler(BaseHandler):
    def post(self):
        cname = self.get_argument('cname')
        if cname == "":
            print('This user name / nodes not exists!!!')
            self.write("wrong format")
            return

        uid = self.get_uid_by_uname(cname)
        if uid == None:
            print('This user name not exists!!!')
            self.write("wrong format")
            return

        self.close_all_container(cname)
        print('rm -rf /public/docker/%s...' % cname)
        os.system('rm -rf /public/docker/%s' % cname)
        print('delete account successfully!!!')

        self.write('ok!')

    def close_all_container(self, cname):
        for node_id in range(1, 18 + 1):
            container_name = '%s.node%.2d' % (cname, node_id)
            os.system('ssh node%.2d "docker stop %s && docker rm %s"' % (node_id, container_name, container_name))

            print('close', container_name, 'done')

        container_name = '%s.admin' % cname
        os.system('docker stop %s && docker rm %s' % (container_name, container_name))
        print('close', container_name, 'done')

    def get_uid_by_uname(self, cname):
        uid = os.popen("grep %s /etc/passwd | cut -f3 -d':'" % cname).read().strip()
        if uid != "":
            return int(uid)
        else:
            return None
