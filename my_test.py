# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午5:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os
from multiprocessing import Pool
import beautiful_output


def main():
    p = Pool(20)
    args_list = [(i,) for i in range(1, 18 + 1)]

    res_list = p.starmap(get_useful_gpu_msg, args_list)

    for res in res_list:
        print(repr(res))
        exit()


def get_useful_gpu_msg(node_id):
    gpu_msg = os.popen("ssh node%.2d /home/piaozx/anaconda3/bin/gpustat -p -u --color" % node_id).read()
    return gpu_msg


if __name__ == '__main__':
    main()
