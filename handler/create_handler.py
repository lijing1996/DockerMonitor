# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午9:59
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os
import json


class CreateHandler(BaseHandler):
    def post(self):
        """
        code 101: blank input!
        code 102: name exists
        code 200: everything is ok
        :return:
        """
        cname = self.get_argument('cname')
        chs_name = self.get_argument('chs_name')
        email = self.get_argument('email')
        ret_data = {'code': '', 'log': ''}
        self.log = ''

        if cname == '' or chs_name == '' or email == '':
            ret_data['code'] = 101
            self.write(ret_data)
            return

        uid = self.db.get_uid_by_username(cname)
        if uid != None:
            ret_data['code'] = 102
            self.write(ret_data)
            return

        uid = self.db.try_to_add_user(cname)

        container_port = uid + 21000
        each_user_port_num = 10
        port_range_str = '%d-%d' % (30000 + each_user_port_num * (uid - 1000), 30000 + each_user_port_num * (uid - 1000 + 1) - 1)
        self.create_user_docker_dir(cname, container_port, port_range_str)
        self.db.add_user(cname, container_port, port_range_str, email, chs_name)
        self.db.add_user_permission(uid, [0], 'yes', '', '', '')

        ret_data['code'] = 200
        ret_data['log'] = self.log
        self.write(ret_data)

    def create_admin_container(self, cname, container_port, port_range_str):
        container_name = '%s.admin' % cname
        print('open-port range:', port_range_str)

        print('Creating user container on admin...')
        os.system("docker run "
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
                  "-p %s:%s "
                  "deepo_plus "
                  "/usr/sbin/sshd -D" % (
                      container_name, cname, cname, cname, cname, cname, cname, cname, cname, cname, cname, container_name, container_port, port_range_str,
                      port_range_str))

    def create_user_docker_dir(self, cname, container_port, port_range_str):
        self.log += 'Creating user docker dir...\n'

        user_dir = '/public/docker/%s' % cname
        if os.path.exists(user_dir):
            print(user_dir, 'exist!!!!')
            self.log += "User docker dir exists!!!, just change user's permission\n"
            return False
        else:
            print('Creating user docker dir...')
            os.system("cp -r /public/docker/baseline-1 %s" % user_dir)
            os.system('''cat /dev/zero | ssh-keygen -q -N "" -f /public/docker/%s/root/.ssh/id_rsa''' % cname)
            os.system("cat /public/docker/%s/root/.ssh/id_rsa.pub >> /public/docker/%s/root/.ssh/authorized_keys" % (cname, cname))
            os.system('sed -i "s/user_port/%d/g" /public/docker/%s/root/.ssh/config' % (container_port, cname))
            os.system('sed -i "s/user_port_range/%s/g" /public/docker/%s/etc/motd' % (port_range_str, cname))
            print('Done.')
            self.log += "user docker dir has been created successfully!\n"

            print('Creating user admin container...')
            self.log += 'Creating user admin container...\n'
            self.create_admin_container(cname, container_port, port_range_str)
            print('Done.')
            self.log += 'Done.\n'

            return True
