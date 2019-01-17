# -*- coding: utf-8 -*-
# @Time    : 2018/9/9 11:22 PM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys

sys.path.append('./')

import os
from db.db_manager import DatabaseManager


class ContainerAdditionStr:

    def __init__(self, node_name, advisor, cname):
        self.node_name = node_name
        self.advisor = advisor
        self.group_mapping = {
            '何旭明': 'plus_group',
            '高盛华': 'svip_group'
        }
        self.username = cname


    def get_node_addition_str(self):
        addition_str = ""
        banned_users = ['yanshp']
        if self.username not in banned_users:
            if self.node_name == 'admin':
                addition_str = ' -v /public/motd/admin_motd:/etc/motd:ro '
            else:
                addition_str = ' -v /public/motd/node_motd:/etc/motd:ro '
        if self.node_name == 'admin':
            addition_str +=  " -m 4G --memory-swap 8G --memory-reservation 2G "
        return addition_str

    def get_advisor_addition_str(self):
        addition_str = ""
        if self.advisor in self.group_mapping:
            group_dir = f'/p300/{self.group_mapping[self.advisor]}'
            readonly_dir = f'/p300/{self.group_mapping[self.advisor]}'
            if not os.path.exists(group_dir):
                os.makedirs(group_dir)
            if not os.path.exists(readonly_dir):
                os.makedirs(readonly_dir)
            addition_str += f' -v {group_dir}:/group ' \
                           f' -v {readonly_dir}:/group/readonly:ro '
        return addition_str

    def get_user_addition_str(self):
        addition_str = ""
        if self.username == "zhangxy" and self.node_name == "admin":
            addition_str += " -v /public/docker/huangshy/root/huangshy/:/root/huangshy "
        return addition_str

    def get_additional_str(self):
        return self.get_node_addition_str() + self.get_advisor_addition_str() + self.get_user_addition_str()

def create_container_on_remote(node_name, docker_type, container_name, cname, shm_size, container_port, add_open_port_str, advisor):
    addition_str = ContainerAdditionStr(node_name, advisor, cname).get_additional_str()

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


def rm_container_on_remote(node_name, container_name, username):
    container_name_with_minus = '%s-%s' % (username, node_name)

    os.system('ssh %s "docker stop %s && docker rm %s"' % (node_name, container_name, container_name))
    print('close', container_name, 'done')


def main():
    db = DatabaseManager()
    user_info_list = db.get_all_user_info()

    for user_info in user_info_list:
        username = user_info['username']
        cname = username
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']
        advisor = user_info['advisor']
        if username != 'wanghz':
            continue
        import pdb;pdb.set_trace()
        for permission_detail in user_info['permission']:
            node_name = permission_detail['name']
            docker_type = 'docker' if node_name == 'admin' else 'nvidia-docker'
            container_name = '%s-%s' % (username, node_name)

            add_open_port_str = "-p %s:%s" % (open_port_range, open_port_range) if node_name == 'admin' else ''

            memory_size = os.popen('''ssh %s  free -h | head -n 2 | tail -n 1 | awk -F' ' '{print $2}' ''' % node_name).read().strip()
            memory_unit = memory_size[-1]
            memory_size = int(memory_size[:-1])
            shm_size = memory_size // 2
            shm_size = str(shm_size) + memory_unit

            rm_container_on_remote(node_name, container_name, username)

            create_container_on_remote(node_name, docker_type, container_name, cname, shm_size, container_port, add_open_port_str, advisor)
            print("create container %s successfully." % container_name)


if __name__ == '__main__':
    main()
