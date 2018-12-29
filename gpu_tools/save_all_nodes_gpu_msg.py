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
from handler.base_handler import STANDARD_NODE_LIST

NODE_LIST = STANDARD_NODE_LIST[1:]


def get_useful_gpu_msg(node_id):
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)
    cursor = conn.cursor()

    while True:
        gpu_msg = os.popen('''ssh node%.2d '/public/anaconda3/bin/python /public/DockerMonitor/gpu_tools/get_gpu_msg.py' ''' % node_id).read().strip()

        cursor.execute('''UPDATE docker.gpu SET node_gpu_msg = '%s' WHERE node_id=%d''' % (gpu_msg, node_id))
        try:
            conn.commit()
            print('node%.2d OK' % node_id)
        except:
            conn.rollback()


def main():
    p = Pool(len(NODE_LIST))
    args_list = [(i,) for i in NODE_LIST]
    p.starmap(get_useful_gpu_msg, args_list)
    p.close()


if __name__ == '__main__':
    main()
