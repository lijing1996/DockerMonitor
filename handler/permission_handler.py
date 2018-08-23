# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午10:47
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import datetime
import os


class PermissionHandler(BaseHandler):
    def get(self):
        user_info_list = self.db.get_all_user_info()

        self.render('../html/permission.html', user_info_list=user_info_list, cur_user=self.get_current_user())

    def post(self):
        """
        add permission for some user
        code 101 : blank input
        code 102 : invalid input longtime
        code 103 : invalid input nodes
        code 104 : user not exists
        code 105 : not long time but don't has start_date and end_date
        code 200 : success
        :return:
        """

        username = self.get_argument('cname')
        str_nodes = self.get_argument('nodes')
        longtime = self.get_argument('longtime')
        start_date = self.get_argument('start')
        end_date = self.get_argument('end')
        reason = self.get_argument('reason')

        ret = {'code': None}
        if username == '' or str_nodes == '':
            ret['code'] = 101
            self.write(ret)
            return

        if longtime not in ['yes', 'no']:
            ret['code'] = 102
            self.write(ret)
            return

        node_list = self.get_node_list_by_str_nodes(str_nodes)
        if node_list == None:
            ret['code'] = 103
            self.write(ret)
            return

        uid = self.db.get_uid_by_username(username)
        if not uid:
            ret['code'] = 104
            self.write(ret)
            return

        if longtime == 'no':
            if start_date == '' or end_date == '':
                ret['code'] = 105
                self.write(ret)
                return
            else:
                start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d') + ' 00:00:00'
                end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d') + ' 23:59:59'

        self.add_user_container(uid, node_list)
        self.db.add_user_permission(uid, node_list, longtime, start_date, end_date, reason)

        ret['code'] = 200
        ret['log'] = self.log
        self.write(ret)

    def add_user_container(self, uid, node_list):
        self.log = ''
        uid, cname, container_port, open_port_range = self.db.get_user_info_by_uid(uid)

        for node_id in node_list:
            print('Creating user container on node%.2d...' % node_id)
            self.log += 'Creating user container on node%.2d...\n' % node_id
            container_name = '%s.node%.2d' % (cname, node_id)
            os.system("ssh node%.2d "
                      "nvidia-docker run "
                      "--name %s "
                      "--pid=host "
                      "-v /home/%s:/home/%s "
                      "-v /public/docker/%s/bin:/bin "
                      "-v /public/docker/%s/etc:/etc "
                      "-v /public/docker/%s/lib:/lib "
                      "-v /public/docker/%s/lib64:/lib64 "
                      "-v /public/docker/%s/opt:/opt "
                      "-v /public/docker/%s/root:/root "
                      "-v /public/docker/%s/sbin:/sbin "
                      "-v /public/docker/%s/usr:/usr "
                      "-h %s "
                      "-d "
                      "-p %d:22 "
                      "deepo_plus "
                      "/usr/sbin/sshd -D" % (
                          node_id, container_name, cname, cname, cname, cname, cname, cname, cname, cname, cname, cname, container_name, container_port))
            print('Done.')
            self.log += 'Done.\n'

        print('create', cname, 'done!', 'port: ', container_port)
        self.log += 'Create %s done! port: %d\n' % (cname, container_port)
        print('add nodes permission successfully')
        self.log += 'add nodes permission on %s successfully\n' % str(node_list)
        print('please login by "ssh root@10.19.124.11 -p %d"\ndefault passwd: plus' % container_port)
        self.log += 'please login by "ssh root@10.19.124.11 -p %d"\ndefault passwd: plus' % container_port
