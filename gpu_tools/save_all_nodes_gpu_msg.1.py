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

from config import DB_HOST, DB_NAME, DB_PASSWOED, DB_USERNAME


def get_useful_gpu_msg(node_id):
    gpu_msg = os.popen('''ssh node%.2d '/public/anaconda3/bin/python /public/DockerMonitor/gpu_tools/get_gpu_msg.py' ''' % node_id).read().strip()

    return gpu_msg


def get_node_msg_list():
    p = Pool(20)
    args_list = [(i,) for i in range(1, 18 + 1)]
    node_gpu_msg_list = p.starmap(get_useful_gpu_msg, args_list)
    p.close()

    return node_gpu_msg_list


def main():
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)
    cursor = conn.cursor()

    while True:
        node_gpu_msg_list = get_node_msg_list()

        try:
            print('-' * 20 + 'start' + '-' * 20)
            for node_id in range(1, 18 + 1):
                print('node%.2d ok' % (node_id))
                cursor.execute('''UPDATE docker.gpu SET node_gpu_msg = '%s' WHERE node_id=%d''' % (node_gpu_msg_list[node_id - 1], node_id))

            conn.commit()
            print('-' * 20 + 'end' + '-' * 20)
        except:
            conn.rollback()
        # time.sleep(1)


if __name__ == '__main__':
    main()
