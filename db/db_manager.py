# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午9:35
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import pymysql
from config import DB_HOST, DB_NAME, DB_PASSWOED, DB_USERNAME
import json


class DatabaseManager:
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME)

    def get_cursor(self):
        try:
            cursor = self.conn.cursor()
        except:
            self.connect()
            cursor = self.conn.cursor()

        return cursor

    def get_all_user_info(self):
        cursor = self.get_cursor()
        cursor.execute("select uid, username,chinese_name,email, container_port, open_port_range from docker.user")
        user_base_list = cursor.fetchall()

        user_info_list = []
        for user_base in user_base_list:
            user_info = {'uid': user_base[0],
                         'username': user_base[1],
                         'chinese_name': user_base[2],
                         'email': user_base[3],
                         'container_port': user_base[4],
                         'open_port_range': user_base[5],
                         'permission': []
                         }

            # query user permission
            cursor.execute("select node_id from docker.permission where uid = %s" % user_info['uid'])
            user_permission_list = cursor.fetchall()
            user_info['permission'] = list(map(lambda x: 'admin' if x[0] == 0 else 'node%.2d' % x[0], user_permission_list))

            user_info_list.append(user_info)

        self.commit()
        return user_info_list

    def add_user(self):
        pass

    def check_user_exist_in_db(self, username):
        cursor = self.get_cursor()
        cursor.execute("select uid from docker.user where username = %s" % username)
        res = cursor.fetchall()
        res = True if len(res) != 0 else False

        self.commit()
        return res

    def delete_user(self):
        pass

    def update_user_permission(self):
        pass

    def get_all_user_lifecycle(self):
        cursor = self.get_cursor()
        cursor.execute("select u.uid, u.username, l.long_time_user, l.start_date, l.end_date, l.reason "
                       "from docker.user u left join docker.lifecycle l on u.uid=l.uid ")
        user_lifecycle_list = cursor.fetchall()

        def format_user_info(user_info):
            long_time_user = True if user_info[2] == 1 else False
            using_date = '%s -- %s' % (user_info[3], user_info[4])

            user_info = {'uid': user_info[0],
                         'username': user_info[1],
                         'lifecycle': 'long time' if long_time_user else using_date,
                         'reason': user_info[5]
                         }

            return user_info

        user_lifecycle_list = list(map(format_user_info, user_lifecycle_list))

        self.commit()
        return user_lifecycle_list

    def get_node_msg_list(self):
        cursor = self.get_cursor()

        cursor.execute("select node_gpu_msg from docker.gpu")
        node_msg_list = cursor.fetchall()
        node_msg_list = map(lambda x: json.loads(x[0]), node_msg_list)
        self.commit()

        return node_msg_list

    def commit(self):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    db_manager = DatabaseManager()
    print(db_manager.check_user_exist_in_db('piaozx'))
