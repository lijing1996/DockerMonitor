# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午9:35
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import pymysql
from config import DB_HOST, DB_NAME, DB_PASSWOED, DB_USERNAME
import json
import datetime


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
            cursor.execute("select node_id,longtime,start_date,end_date, reason from docker.permission where uid = %s" % user_info['uid'])
            user_permission_list = cursor.fetchall()

            for user_permission in user_permission_list:
                node_id, longtime, start_date, end_date, reason = user_permission
                if longtime == 0:
                    start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
                    end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

                node_info = {'name': 'admin' if node_id == 0 else 'node%.2d' % node_id,
                             'longtime': longtime,
                             'start_date': start_date,
                             'end_date': end_date,
                             'reason': reason
                             }
                user_info['permission'].append(node_info)

            user_info_list.append(user_info)

        self.commit()
        return user_info_list

    def get_user_info_by_uid(self, uid):
        cursor = self.get_cursor()
        cursor.execute("select uid, username, container_port, open_port_range from docker.user where uid=%s" % uid)
        user_info = cursor.fetchone()

        self.commit()
        return user_info

    def try_to_add_user(self, username):
        '''
        before add user, we try to add user for uid
        '''
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO docker.user(username) VALUES ('%s')" % username)
        cursor.execute("SELECT uid from docker.user where username = '%s'" % username)
        uid = cursor.fetchone()
        uid = uid[0] if uid else None

        self.commit()
        return uid

    def add_user(self, username, container_port, open_port_range, email, chinese_name):
        '''
        add_user actually is update operator
        '''
        cursor = self.get_cursor()
        cursor.execute("UPDATE docker.user SET container_port = %s, open_port_range = '%s', email = '%s', chinese_name = '%s' WHERE username = '%s'"
                       % (container_port, open_port_range, email, chinese_name, username))

        self.commit()

    def get_uid_by_username(self, username):
        cursor = self.get_cursor()
        cursor.execute("select uid from docker.user where username = '%s'" % username)
        uid = cursor.fetchone()
        uid = uid[0] if uid else None

        self.commit()
        return uid

    def delete_user(self):
        pass

    def remove_user_permission(self, uid, node_list):
        cursor = self.get_cursor()
        node_list = tuple(node_list + [100])
        cursor.execute("delete from docker.permission where uid = %s and node_id in %s" % (uid, node_list))

        self.commit()

    def add_user_permission(self, uid, node_list, long_time, start_date, end_date, reason):
        """
        :param uid: int
        :param node_list: list
        :param long_time: 'yes' or 'no'
        :return:
        """
        cursor = self.get_cursor()

        cursor.execute("SELECT node_id from docker.permission where uid=%s" % uid)
        exist_node_list = cursor.fetchall()

        exist_node_list = list(map(lambda x: x[0], exist_node_list))
        node_list = filter(lambda x: x not in exist_node_list, node_list)

        if long_time == 'yes':
            for node_id in node_list:
                cursor.execute("INSERT INTO docker.permission(uid, node_id, reason) "
                               "VALUES (%s, %s, '%s')" % (uid, node_id, reason))
        else:
            for node_id in node_list:
                cursor.execute("INSERT INTO docker.permission(uid, node_id, longtime, start_date, end_date, reason) "
                               "VALUES (%s, %s, 0, '%s', '%s', '%s')" % (uid, node_id, start_date, end_date, reason))

        self.commit()
        return node_list

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

    '''
    for discuss
    '''

    def add_question(self, title, content, create_date):
        cursor = self.get_cursor()

        cursor.execute("INSERT INTO docker.discuss(title, content, create_date) VALUES ('%s', '%s','%s')" % (title, content, create_date))
        self.commit()

    def add_answer(self, question_id, content, create_date):
        cursor = self.get_cursor()

        cursor.execute("SELECT max(floor) from docker.answer where question_id= %d" % question_id)
        max_floor = cursor.fetchone()[0]
        if max_floor == None:
            floor = 1
        else:
            floor = max_floor + 1

        cursor.execute(
            "INSERT INTO docker.answer(question_id, floor,content, create_date) VALUES (%d, %d, '%s','%s')" % (question_id, floor, content, create_date))
        self.commit()

    def get_all_questions(self):
        cursor = self.get_cursor()

        cursor.execute("select question_id, title, create_date  from docker.discuss")
        question_list = cursor.fetchall()

        self.commit()
        return question_list

    def get_all_answer_by_question_id(self, question_id):
        cursor = self.get_cursor()

        cursor.execute("select title, content, create_date from docker.discuss where question_id = %d" % question_id)
        title, question_content, create_date = cursor.fetchone()

        cursor.execute("select floor, content, create_date from docker.answer where question_id = %d" % question_id)
        answer_list = cursor.fetchall()

        self.commit()
        return title, question_content, create_date, answer_list

    def check_question_exist_in_db(self, question_id):
        cursor = self.get_cursor()

        cursor.execute("select question_id from docker.discuss where question_id = %d" % question_id)
        res = cursor.fetchall()
        res = True if len(res) != 0 else False

        self.commit()
        return res

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
