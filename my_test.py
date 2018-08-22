# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午5:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os
import json
from multiprocessing import Pool
import beautiful_output


def main():
    a = '''{"hostname": "compute101", "query_time": "2018-08-22T23:04:16.644530", "gpus": [{"index": 0, "uuid": "GPU-2494c1b5-ef37-b31d-94cb-d41590a93477", "name": "Tesla M40 24GB", "temperature.gpu": 57, "utilization.gpu": 98, "power.draw": 189, "enforced.power.limit": 250, "memory.used": 1126, "memory.total": 22939, "processes": [{"username": "lijing", "command": "python", "gpu_memory_usage": 1115, "pid": 10758, "runtime": "03:07:51"}]}, {"index": 1, "uuid": "GPU-b05d2d0e-b792-6b0f-d7b0-a46158e83ea6", "name": "Tesla M40 24GB", "temperature.gpu": 57, "utilization.gpu": 98, "power.draw": 185, "enforced.power.limit": 250, "memory.used": 1126, "memory.total": 22939, "processes": [{"username": "lijing", "command": "python", "gpu_memory_usage": 1115, "pid": 11099, "runtime": "03:05:57"}]}, {"index": 2, "uuid": "GPU-b3dedd32-1e1f-7aca-6de4-592f16308ccd", "name": "Tesla M40 24GB", "temperature.gpu": 57, "utilization.gpu": 99, "power.draw": 185, "enforced.power.limit": 250, "memory.used": 1126, "memory.total": 22939, "processes": [{"username": "lijing", "command": "python", "gpu_memory_usage": 1115, "pid": 11339, "runtime": "03:04:18"}]}, {"index": 3, "uuid": "GPU-f6e9e731-f5a0-9f7a-edb4-363227cbc275", "name": "Tesla M40 24GB", "temperature.gpu": 59, "utilization.gpu": 99, "power.draw": 231, "enforced.power.limit": 250, "memory.used": 1984, "memory.total": 22939, "processes": [{"username": "lijing", "command": "python", "gpu_memory_usage": 1973, "pid": 11842, "runtime": "03:01:51"}]}]}  '''

    a = json.loads(a)
    print(a)

if __name__ == '__main__':
    main()
