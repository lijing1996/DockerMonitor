# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午9:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os
import json
import socket
import sqlite3
import time
from multiprocessing import Pool


def get_user_name_and_run_time(pid):
    stdout = os.popen("ps -p %s -o user= -o etime=" % pid).read()
    if stdout == '':
        user_name, run_time = 'dead', 'dead'
    else:
        user_name, run_time = stdout.split()
        run_time = list(run_time)

        run_time[-3] = '分钟'

        if len(run_time) > 5:
            run_time[-6] = '小时'
        run_time = ''.join(run_time)
        run_time = run_time.replace('-', '天')
        run_time += '秒'

    user_name = user_name.strip()
    run_time = run_time.strip()

    return user_name, run_time


def get_node_gpu_msg():
    gpu_msg_list = os.popen("gpustat -p -u --json").read()
    gpu_msg_list = json.loads(gpu_msg_list)

    for gpu_msg in gpu_msg_list['gpus']:
        for process in gpu_msg['processes']:
            user_name, run_time = get_user_name_and_run_time(process['pid'])
            process['username'] = user_name
            process['runtime'] = run_time

    node_gpu_msg = json.dumps(gpu_msg_list, ensure_ascii=False)

    hostname = socket.gethostname()
    node_id = int(hostname[8:])

    return node_id, node_gpu_msg


def main():
    conn = sqlite3.connect('gpu.sqlite')

    while True:
        try:
            node_id, node_gpu_msg = get_node_gpu_msg()
            print(node_gpu_msg)
            c = conn.cursor()

            c.execute("UPDATE p40_gpu SET node_gpu_msg = '%s' WHERE node_id=%d" % (node_gpu_msg, node_id))
            conn.commit()

        except Exception as e:
            print(e)
            print('mysql rollback')
            conn.rollback()

        time.sleep(0.5)


if __name__ == '__main__':
    main()
