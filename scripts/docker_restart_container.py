# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 11:58 AM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os


def main():
    node_name_list = ['node%.2d' % i for i in range(1, 18 + 1)] + ['admin']

    for node_name in node_name_list:
        os.system("ssh %s 'docker start $(docker ps -a -q -f status=exited)' " % node_name)


if __name__ == '__main__':
    main()
