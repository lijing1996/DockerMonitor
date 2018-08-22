# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午11:20
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os
import datetime


class DiscussHandler(BaseHandler):
    def get(self):
        question_id = self.get_argument('question_id', None)
        if question_id == None or not self.db.check_question_exist_in_db(int(question_id)):
            question_list = self.db.get_all_questions()
            self.render('../html/discuss.html', question_list=question_list, cur_user=self.get_current_user())
        else:
            question_id = int(question_id)
            title, question_content, create_date, answer_list = self.db.get_all_answer_by_question_id(question_id)

            self.render('../html/answer.html', title=title, question_content=question_content, create_date=create_date, answer_list=answer_list,
                        question_id=question_id, cur_user=self.get_current_user())

    def post(self):
        msg_type = self.get_argument('type')
        if msg_type == 'issue':
            '''
            code 101 : blank input 
            code 102 : has single quote
            code 200 : success
            '''
            title = self.get_argument('title')
            content = self.get_argument('content')
            create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            ret = {'code': None}

            if title == "" or content == "":
                ret['code'] = 101
                self.write(ret)
                return

            elif title.find("'") != -1 or content.find("'") != -1:
                ret['code'] = 102
                self.write(ret)
                return

            self.db.add_question(title, content, create_date)

            ret['code'] = 200
            self.write(ret)
        elif msg_type == 'answer':
            '''
            code 101 : blank input 
            code 102 : has single quote
            code 200 : success
            '''
            question_id = int(self.get_argument('question_id'))
            content = self.get_argument('content')
            create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            ret = {'code': None}

            if question_id == "" or content == "":
                ret['code'] = 101
                self.write(ret)
                return

            elif content.find("'") != -1:
                ret['code'] = 102
                self.write(ret)
                return

            self.db.add_answer(question_id, content, create_date)

            ret['code'] = 200
            self.write(ret)
