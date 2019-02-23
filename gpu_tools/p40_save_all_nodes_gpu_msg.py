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
WATCH_NODES_ID_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]


# WATCH_NODES_ID_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def get_node_msg_list(sqlite_conn):
    try:
        sqlite_cur = sqlite_conn.cursor()
        res = sqlite_cur.execute('SELECT node_id, node_gpu_msg from p40_gpu where node_gpu_msg <> ""')
        sqlite_conn.commit()
    except Exception as e:
        print(e)
        print('sqlite_conn rollback')
        sqlite_conn.rollback()
        return get_node_msg_list(sqlite_conn)

    return res


def check_and_restart_pbs_task():
    # node status 'busy*' or 'free'
    node_status_list = os.popen(" pestat | grep 'sist-gpu' | awk -F' ' '{print $2}' ").read().split()
    node_status_list = [None] + node_status_list

    # node run 'C' 'Q' 'R'
    node_run_str_list = os.popen('''  qstat | grep 'sist-gpu' | awk -F' ' '{print $2 " " $5}'  ''').read().replace('sist-gpu', '').split()
    node_run_list = ['C'] * 29

    for i in range(len(node_run_str_list) // 2):
        try:
            node_id = int(node_run_str_list[2 * i])
            node_run = node_run_str_list[2 * i + 1]
            node_run_list[node_id] = node_run
        except:
            continue

    # restart cancelled task
    for node_id in WATCH_NODES_ID_LIST:
        status = node_status_list[node_id]
        run = node_run_list[node_id]

        if status == 'free' and run == 'C':
            os.popen("qsub -N sist-gpu%.2d -q sist-gaoshh -l nodes=sist-gpu%.2d:ppn=1 -o /dev/null -e /dev/null gpu.pb" % (node_id, node_id))


def main():
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)
    cursor = conn.cursor()

    sqlite_conn = sqlite3.connect('gpu.sqlite')

    while True:

        try:
            node_gpu_msg_list = get_node_msg_list(sqlite_conn)
            check_and_restart_pbs_task()

            print('-' * 20 + 'start' + '-' * 20)
            for node_id, node_gpu_msg in node_gpu_msg_list:
                print('node%.2d ok' % (node_id))
                cursor.execute('''UPDATE docker.p40_gpu SET node_gpu_msg = '%s' WHERE node_id=%d''' % (node_gpu_msg, node_id))

            conn.commit()
            print('-' * 20 + 'end' + '-' * 20)
        except Exception as e:
            print(e)
            print('mysql rollback')
            conn.rollback()
        time.sleep(0.2)


if __name__ == '__main__':
    main()
