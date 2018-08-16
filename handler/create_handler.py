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
        code 101: name not exists
        code 102: wrong nodes or not exists

        code 200: everything is ok
        :return:
        """
        cname = self.get_argument('cname')
        nodes = self.get_argument('nodes')
        ret_data = {'code': '', 'log': ''}
        self.log = ''

        uid = self.get_uid_by_uname(cname)
        if uid == None:
            print('name not exists')
            ret_data['code'] = 101
            ret_data['log'] = 'name not exists'
            self.write(ret_data)
            return

        node_list = self.get_node_list_by_str_nodes(nodes)
        if node_list == None:
            print('wrong nodes or not exists')
            ret_data['code'] = 102
            ret_data['log'] = 'wrong nodes or not exists'
            self.write(ret_data)
            return

        ret_data['code'] = 200
        container_port = uid + 21000
        each_user_port_num = 10
        port_range_str = '%d-%d' % (30000 + each_user_port_num * (uid - 1000), 30000 + each_user_port_num * (uid - 1000 + 1) - 1)
        self.create_user_docker_dir(cname, container_port, port_range_str)

        for node_id in nodes:
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
        self.log += 'add nodes permission on %s successfully\n' % str(nodes)
        print('please login by "ssh root@10.19.124.11 -p %d"\ndefault passwd: plus' % container_port)
        self.log += 'please login by "ssh root@10.19.124.11 -p %d"\ndefault passwd: plus' % container_port

        self.db.add_user()

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
