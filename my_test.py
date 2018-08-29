# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午5:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os
import json
from multiprocessing import Pool
import beautiful_output
import datetime
import pymysql
from config import *


def main():
    node_list = range(1, 18 + 1)
    name_to_node_dict = {}

    for i in node_list:
        with open('/public/nodes/%.2d.usr' % i, 'r') as f:
            usr_list = f.read().split()
            for usr in usr_list:
                if usr not in name_to_node_dict.keys():
                    name_to_node_dict[usr] = [i]
                else:
                    name_to_node_dict[usr].append(i)

    for name, node_list in name_to_node_dict.items():
        print('%s: %s' % (name, node_list))

    print(len(name_to_node_dict))


if __name__ == '__main__':
    main()
