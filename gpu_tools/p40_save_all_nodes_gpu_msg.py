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
import sqlite3

DB_HOST = '10.19.124.11'
DB_USERNAME = 'root'
DB_PASSWOED = 'piaozx123'
DB_NAME = 'docker'


def get_node_msg_list(sqlite_conn):
    sqlite_cur = sqlite_conn.cursor()
    res = sqlite_cur.execute('SELECT node_id, node_gpu_msg from p40_gpu where node_gpu_msg <> ""')
    sqlite_conn.commit()

    return res




def main():
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)
    cursor = conn.cursor()

    sqlite_conn = sqlite3.connect('gpu.sqlite')


    while True:
        node_gpu_msg_list = get_node_msg_list(sqlite_conn)

        try:
            print('-' * 20 + 'start' + '-' * 20)
            for node_id, node_gpu_msg in node_gpu_msg_list:
                print('node%.2d ok' % (node_id))
                cursor.execute('''UPDATE docker.p40_gpu SET node_gpu_msg = '%s' WHERE node_id=%d''' % (node_gpu_msg, node_id))

            conn.commit()
            print('-' * 20 + 'end' + '-' * 20)
        except:
            print('rollback')
            conn.rollback()
        time.sleep(0.2)


if __name__ == '__main__':
    main()
