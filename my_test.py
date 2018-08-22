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
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)
    cursor = conn.cursor()

    question_id = 1
    cursor.execute("SELECT max(floor) from docker.answer where question_id= %d" % question_id)
    max_floor = cursor.fetchone()

    print(max_floor)

if __name__ == '__main__':
    main()
