# -*- coding: utf-8 -*-
# @Time    : 2018/10/2 12:02 AM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys

sys.path.append('./')

import os
from db.db_manager import DatabaseManager


def rm_container_on_remote(node_name, container_name):
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

        if os.path.exists('/p300/docker/%s/root/.ssh/config' % username):
            os.system("rm /p300/docker/%s/root/.ssh/config" % username)
            os.system("cp /p300/docker/baseline-1/root/.ssh/config /p300/docker/%s/root/.ssh/config" % username)
            os.system('sed -i "s/user_port/%d/g" /p300/docker/%s/root/.ssh/config' % (container_port, cname))

            print("update %s successfully." % username)


if __name__ == '__main__':
    main()
