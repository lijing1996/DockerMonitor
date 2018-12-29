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


def change_prepared_basline():
    prepared_root_path = '/public/docker/prepare_baseline-1'

    for prepared_dir_name in os.listdir(prepared_root_path):
        os.system('rm %s/%s/root/.ssh/config ' % (prepared_root_path, prepared_dir_name))
        os.system("cp /public/docker/baseline-1/root/.ssh/config %s/%s/root/.ssh/config" % (prepared_root_path, prepared_dir_name))

        print("update %s successfully." % prepared_dir_name)


def main():
    db = DatabaseManager()
    user_info_list = db.get_all_user_info()

    for user_info in user_info_list:
        username = user_info['username']
        cname = username
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']

        # if username not in  ['piaozx']:
        #     continue

        if os.path.exists('/public/docker/%s/root/.ssh/config' % username):
            os.system("rm /public/docker/%s/root/.ssh/config" % username)
            os.system("cp /public/docker/baseline-1/root/.ssh/config /public/docker/%s/root/.ssh/config" % username)
            os.system('sed -i "s/user_port/%d/g" /public/docker/%s/root/.ssh/config' % (container_port, cname))

            print("update %s successfully." % username)


if __name__ == '__main__':
    # change_prepared_basline()
    main()
