# -*- coding: utf-8 -*-
# @Time    : 2019-02-24 12:49
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys

sys.path.append('./')

import os
from db.db_manager import DatabaseManager
from multiprocessing import Pool
from utils import utils


def create_container_on_remote(node_name, docker_type, container_name, cname, shm_size, container_port, addition_str):
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
                  node_name, docker_type, container_name, cname, cname, cname, cname, cname, cname, cname, cname, cname, container_name, shm_size,
                  addition_str, container_name, container_port))

    print("create container on %s successful!" % node_name)


def remove_container_on_remote(node_name, container_name):
    os.system('ssh %s "docker stop %s && docker rm %s"' % (node_name, container_name, container_name))
    print('close', container_name, 'done')


def remove_container_on_remote_by_node_list(need_remove_node_list, db, uid, username):
    if len(need_remove_node_list) == 0:
        return

    p = Pool(len(need_remove_node_list))
    args_list = []

    for node_id in need_remove_node_list:
        node_name = 'admin' if node_id == 0 else 'node%.2d' % node_id
        container_name = '%s-%s' % (username, node_name)
        args_list.append((node_name, container_name))

    p.starmap(remove_container_on_remote, args_list)
    p.close()

    db.remove_user_permission(uid, need_remove_node_list)


def main():
    db = DatabaseManager()
    user_info_list = db.get_all_user_info()

    svip_node_list = [1, 2, 5, 17, 18, 19, 20, 24, 29, 30]
    public_node_list = [13, 14, 26, 23, 32, 33, 15, 16]
    new_node_list = svip_node_list + public_node_list

    for user_info in user_info_list:
        uid = user_info['uid']
        username = user_info['username']
        cname = username
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']
        advisor = user_info['advisor']

        """
        SVIP Lab
        """
        if advisor != '高盛华':
            continue

        if username not in ['xuyy']:
            continue

        exist_compute_node_list = []
        for node_info in user_info['permission']:
            node_name = node_info['name']
            if node_name == 'admin':
                continue
            else:
                node_id = int(node_name[4:])
            exist_compute_node_list.append(node_id)

        need_remove_node_list = list(set(exist_compute_node_list) - set(new_node_list))
        remove_container_on_remote_by_node_list(need_remove_node_list, db, uid, username)

        need_add_node_list = list(set(new_node_list) - set(exist_compute_node_list))

        for node_id in need_add_node_list:
            node_name = 'node%.2d' % node_id
            docker_type = 'docker' if node_name == 'admin' else 'nvidia-docker'
            container_name = '%s_%s' % (username, node_name)

            add_open_port_str = "-p %s:%s" % (open_port_range, open_port_range) if node_name == 'admin' else ''

            memory_size = os.popen('''ssh %s  free -h | head -n 2 | tail -n 1 | awk -F' ' '{print $2}' ''' % node_name).read().strip()
            memory_unit = memory_size[-1]
            memory_size = int(memory_size[:-1])
            shm_size = memory_size // 2
            shm_size = str(shm_size) + memory_unit

            addition_str = utils.ContainerAdditionStr(node_name, advisor, cname).get_additional_str()
            create_container_on_remote(node_name, docker_type, container_name, cname, shm_size, container_port, addition_str)
            print("create container %s successfully." % container_name)

        db.add_user_permission(uid, need_add_node_list, 'yes', '', '', '')


if __name__ == '__main__':
    main()
