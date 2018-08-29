# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午10:03
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys
import os

sys.path.append(os.path.abspath('./'))

from multiprocessing import Pool
import json
import pymysql
import time

DB_HOST = '10.19.124.11'
DB_USERNAME = 'root'
DB_PASSWOED = 'piaozx123'
DB_NAME = 'docker'
node_range = [9, 10, 11, 12, 13,14,15, 16, 17, 18, 28]


def get_useful_gpu_msg(node_id):
    gpu_msg = os.popen('''ssh node%.2d 'python DockerMonitor/gpu_tools/p40_get_gpu_msg.py' ''' % node_id).read().strip()

    return gpu_msg


def get_node_msg_list():
    p = Pool(len(node_range))
    args_list = [(i,) for i in node_range]
    node_gpu_msg_list = p.starmap(get_useful_gpu_msg, args_list)
    p.close()

    return node_gpu_msg_list


def main():
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)
    cursor = conn.cursor()

    while True:
        node_gpu_msg_list = get_node_msg_list()
        # node_range = [7, 8, 9, 10, 11, 12]

        try:
            print('-' * 20 + 'start' + '-' * 20)
            for node_id, node_gpu_msg in zip(node_range, node_gpu_msg_list):
                print('node%.2d ok' % (node_id))
                cursor.execute('''UPDATE docker.p40_gpu SET node_gpu_msg = '%s' WHERE node_id=%d''' % (node_gpu_msg, node_id))

            conn.commit()
            print('-' * 20 + 'end' + '-' * 20)
        except:
            print('rollback')
            conn.rollback()
        # time.sleep(1)


if __name__ == '__main__':
    main()
