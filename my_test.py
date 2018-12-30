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

import sqlite3
import socket


def main():
    node_list = range(2, 36)

    for node in node_list:
        os.system('''ssh node%.2d "docker stop \$(docker ps -aq)"''' % node)
        os.system('''ssh node%.2d "docker rm \$(docker ps -aq)"''' % node)


if __name__ == '__main__':
    main()
