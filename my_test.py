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
    a = set([1,2,3])
    b = set([2,3,4])

    print(a - b)


if __name__ == '__main__':
    main()
