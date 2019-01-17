# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午9:59
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os
import json
from utils import utils

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
        advisor = self.get_argument('advisor')
        ret_data = {'code': '', 'log': ''}
        self.log = ''

        if cname == '' or chs_name == '' or email == '' or advisor == '':
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
        self.create_user_docker_dir(cname, container_port, port_range_str, advisor)
        self.db.add_user(cname, container_port, port_range_str, email, chs_name, advisor)
        self.db.add_user_permission(uid, [0], 'yes', '', '', '')

        ret_data['code'] = 200
        ret_data['log'] = self.log
        self.write(ret_data)

    def create_admin_container(self, cname, container_port, port_range_str, advisor):
        container_name = '%s-admin' % cname
        print('open-port range:', port_range_str)

        memory_size = os.popen('''free -h | head -n 2 | tail -n 1 | awk -F' ' '{print $2}' ''').read().strip()
        memory_unit = memory_size[-1]
        memory_size = int(memory_size[:-1])
        shm_size = memory_size // 2
        shm_size = str(shm_size) + memory_unit
        addition_str = utils.ContainerAdditionStr(node_name, advisor, cname).get_additional_str()

        print('Creating user container on admin...')
        os.system("ssh %s "
              "%s run "
              "--name %s "
              "--network=host "
              "-v /p300/docker/%s:/p300 "
              "-v /p300/datasets:/datasets:ro "
              "-v /public/docker/%s/bin:/bin "
              "-v /public/docker/%s/etc:/etc "
              "-v /public/docker/%s/lib:/lib "
              "-v /public/docker/%s/lib64:/lib64 "
              "-v /public/docker/%s/opt:/opt "
              "-v /public/docker/%s/root:/root "
              "-v /public/docker/%s/sbin:/sbin "
              "-v /public/docker/%s/usr:/usr "
              # "--privileged=true "
              # "--volume /run/dbus/system_bus_socket:/run/dbus/system_bus_socket:ro "
              "--restart unless-stopped "
              "--add-host %s:127.0.0.1 "
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
              "--add-host node19:10.10.10.119 "
              "--add-host node20:10.10.10.120 "
              "--add-host node21:10.10.10.121 "
              "--add-host node22:10.10.10.122 "
              "--add-host node23:10.10.10.123 "
              "--add-host node24:10.10.10.124 "
              "--add-host node25:10.10.10.125 "
              "--add-host node26:10.10.10.126 "
              "--add-host node27:10.10.10.127 "
              "--add-host node28:10.10.10.128 "
              "--add-host node29:10.10.10.129 "
              "--add-host node30:10.10.10.130 "
              "--add-host node31:10.10.10.131 "
              "--add-host node32:10.10.10.132 "
              "--add-host node33:10.10.10.133 "
              "--add-host node34:10.10.10.134 "
              "--add-host node35:10.10.10.135 "
              "--add-host admin:10.10.10.100 "
              "--shm-size=%s "
              "%s "
              "-h %s "
              "-d "
              "deepo_plus "
              "/usr/sbin/sshd -p %d -D" % (
                  node_name, docker_type, container_name, cname, cname, cname, cname, cname, cname, cname, cname, cname, container_name, shm_size, addition_str,
                  container_name, container_port))
        print("create container on %s successful!" % node_name)

    def create_user_docker_dir(self, cname, container_port, port_range_str, advisor):
        self.log += 'Creating user docker dir...\n'

        user_dir = '/public/docker/%s' % cname
        if os.path.exists(user_dir):
            print(user_dir, 'exist!!!!')
            self.log += "User docker dir exists!!!, just change user's permission\n"
            return False
        else:
            prepare_root_path = '/public/docker/prepare_baseline-1'
            prepare_dirname_list = sorted(os.listdir(prepare_root_path))

            print('Creating user docker dir...')
            if len(prepare_dirname_list) == 0:
                os.system("cp -r /public/docker/baseline-1 %s" % user_dir)
            else:
                prepare_dir = '%s/%s' % (prepare_root_path, prepare_dirname_list[0])
                print("mv %s %s" % (prepare_dir, user_dir))
                os.system("mv %s %s" % (prepare_dir, user_dir))

            # build ssh-key
            os.system('''cat /dev/zero | ssh-keygen -q -N "" -f /public/docker/%s/root/.ssh/id_rsa''' % cname)
            os.system("cat /public/docker/%s/root/.ssh/id_rsa.pub >> /public/docker/%s/root/.ssh/authorized_keys" % (cname, cname))
            os.system('sed -i "s/user_port/%d/g" /public/docker/%s/root/.ssh/config' % (container_port, cname))
            os.system('sed -i "s/user_port_range/%s/g" /public/docker/%s/etc/motd' % (port_range_str, cname))
            print('Done.')
            self.log += "user docker dir has been created successfully!\n"

            print('Creating user admin container...')
            self.log += 'Creating user admin container...\n'
            self.create_admin_container(cname, container_port, port_range_str, advisor)
            print('Done.')
            self.log += 'Done.\n'

            return True
