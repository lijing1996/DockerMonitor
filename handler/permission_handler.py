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
        code 105 : not long time but doesn't have start_date and end_date
        code 106 : not long time but doesn't have reason
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
            elif reason == '':
                ret['code'] = 106
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
            docker_type = 'docker' if node_id == 0 else 'nvidia-docker'
            node_name = 'admin' if node_id == 0 else 'node%.2d' % node_id
            add_open_port_str = "-p %s:%s" % (open_port_range, open_port_range) if node_id == 0 else ''

            container_name = '%s.%s' % (cname, node_name)
            print('Creating user container on %s...' % node_name)
            self.log += 'Creating user container on node%s...\n' % node_name
            os.system("ssh %s "
                      "%s run "
                      "--name %s "
                      "-v /home/%s:/home/%s "
                      "-v /public/docker/%s/bin:/bin "
                      "-v /public/docker/%s/etc:/etc "
                      "-v /public/docker/%s/lib:/lib "
                      "-v /public/docker/%s/lib64:/lib64 "
                      "-v /public/docker/%s/opt:/opt "
                      "-v /public/docker/%s/root:/root "
                      "-v /public/docker/%s/sbin:/sbin "
                      "-v /public/docker/%s/usr:/usr "
                      "--add-host node01:10.10.10.101 "
                      "--add-host node02:10.10.10.102 "
                      "--add-host node03:10.10.10.103 "
                      "--add-host node04:10.10.10.104 "
                      "--add-host node05:10.10.10.105 "
                      "--add-host node06:10.10.10.106 "
                      "--add-host node07:10.10.10.107 "
                      "--add-host node08:10.10.10.108 "
                      "--add-host node09:10.10.10.109 "
                      "--add-host node10:10.10.10.110 "
                      "--add-host node11:10.10.10.111 "
                      "--add-host node12:10.10.10.112 "
                      "--add-host node13:10.10.10.113 "
                      "--add-host node14:10.10.10.114 "
                      "--add-host node15:10.10.10.115 "
                      "--add-host node16:10.10.10.116 "
                      "--add-host node17:10.10.10.117 "
                      "--add-host node18:10.10.10.118 "
                      "--add-host admin:10.10.10.100 "
                      "-h %s "
                      "-d "
                      "-p %d:22 "
                      "%s "
                      "deepo_plus "
                      "/usr/sbin/sshd -D" % (
                          node_name, docker_type, container_name, cname, cname, cname, cname, cname, cname, cname, cname, cname, cname, container_name,
                          container_port, add_open_port_str))
            print('Done.')
            self.log += 'Done.\n'

        print('create', cname, 'done!', 'port: ', container_port)
        self.log += 'Create %s done! port: %d\n' % (cname, container_port)
        print('add nodes permission successfully')
        self.log += 'add nodes permission on %s successfully\n' % str(node_list)
        print('please login by "ssh root@10.19.124.11 -p %d"\ndefault passwd: plus' % container_port)
        self.log += 'please login by "ssh root@10.19.124.11 -p %d"\ndefault passwd: plus' % container_port
