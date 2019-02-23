# -*- coding: utf-8 -*-
# @Time    : 2019-02-22 23:50
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import requests
import json
import smtplib
import time
import os
from email.mime.text import MIMEText
from email.header import Header
from db.db_manager import DatabaseManager
from config import mail_host, mail_user, mail_pass


def convert_chinese_runtime_to_second(chinese_runtime):
    chinese_time_units = ['天', '小时', '分钟', '秒']
    convert_second_times = [86400, 3600, 60, 1]

    total_second = 0
    for i, chinese_time_unit in enumerate(chinese_time_units):
        idx = chinese_runtime.find(chinese_time_unit)
        if idx != -1:
            num = int(chinese_runtime[:idx])
            total_second += convert_second_times[i] * num
            chinese_runtime = chinese_runtime[idx + len(chinese_time_unit):]

    return total_second


def get_current_user_process_info_dict(db):
    node_gpu_msg_list = db.get_node_msg_list()

    user_process_info_dict = {}

    for node_gpu_msg in node_gpu_msg_list:
        hostname = node_gpu_msg['hostname']

        for gpu in node_gpu_msg['gpus']:
            gpu_id = gpu['index']
            for process_info in gpu['processes']:
                user_container_name = process_info['username']
                username = user_container_name.split('-node')[0]
                pid = process_info['pid']
                runtime = process_info['runtime']
                runtime = convert_chinese_runtime_to_second(runtime)

                card_id = '%s_%s' % (hostname, gpu_id)
                p_info = {'hostname': hostname, 'gpu_id': gpu_id, 'pid': pid, 'runtime': runtime}

                if username not in user_process_info_dict:
                    user_process_info_dict[username] = {card_id: [p_info]}
                elif card_id not in user_process_info_dict[username]:
                    user_process_info_dict[username][card_id] = [p_info]
                else:
                    user_process_info_dict[username][card_id].append(p_info)

    return user_process_info_dict


def get_sorted_card_info_list(process_info):
    sorted_card_info_list = []
    for card_id, p_info_list in process_info.items():
        sorted_card_info_list.append(p_info_list)

    sorted_card_info_list = sorted(sorted_card_info_list, key=lambda x: max(x, key=lambda x: x['runtime'])['runtime'], reverse=True)
    return sorted_card_info_list


def kill_process_by_p_info(p_info, history_p_info_dict):
    fused_pid = '%s-%s' % (p_info['hostname'], p_info['pid'])
    if fused_pid in history_p_info_dict:
        return
    os.system("ssh %s kill -9 %s" % (p_info['hostname'], p_info['pid']))


def send_email(user_info, used_card_num, soft_max_card_num, hard_max_card_num, soft_time):
    sender = 'piaozhx@shanghaitech.edu.cn'
    receiver = user_info['email']
    username = user_info['username']

    if receiver in ['test', 'NA', '']:
        return

    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_content = '''
        Hi, %s:
            你的用卡数量(%d) 已经超过规定数量(%d), 请及时下线不必要的程序, 超过的部分将于%d秒后自动关闭.
            注意, 如果你的用卡数量超过%d张, 多出的部分将会被立即关闭.
            
    Best Wishes 
    AI集群运维团队
        ''' % (username, used_card_num, soft_max_card_num, soft_time, hard_max_card_num)

    message = MIMEText(mail_content, 'plain', 'utf-8')
    message['From'] = Header("AI集群管理", 'utf-8')
    message['To'] = Header("AI集群用户", 'utf-8')
    message['Subject'] = Header('AI集群过载提醒', 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)  # 25 为 SMTP 端口号

        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()

        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("%s 邮件发送成功" % receiver)
        return True

    except smtplib.SMTPException:
        print("Error: %s 无法发送邮件" % receiver)
        time.sleep(10)
        send_email(user_info, used_card_num, soft_max_card_num, hard_max_card_num, soft_time)


def get_history_p_info_dict(db):
    current_user_process_info_dict = get_current_user_process_info_dict(db)

    history_p_info_dict = {}
    for user, process_info in current_user_process_info_dict.items():
        for card_id, p_info_list in process_info.items():
            for p_info in p_info_list:
                hostname = p_info['hostname']
                pid = p_info['pid']
                fused_pid = '%s-%s' % (hostname, pid)

                history_p_info_dict[fused_pid] = 1

    return history_p_info_dict


def convert_user_info_list_to_dict(user_info_list):
    user_info_dict = {}
    for user_info in user_info_list:
        user_info_dict[user_info['username']] = user_info

    return user_info_dict


def main():
    soft_max_card_num = 8
    hard_max_card_num = 20
    soft_time = 3600

    db = DatabaseManager()
    middle_user_dict = {}

    history_p_info_dict = get_history_p_info_dict(db)

    while True:
        current_user_process_info_dict = get_current_user_process_info_dict(db)
        user_info_list = db.get_all_user_info()
        user_info_dict = convert_user_info_list_to_dict(user_info_list)

        for user, process_info in current_user_process_info_dict.items():
            if user not in user_info_dict:
                continue

            permission_num = len(user_info_dict[user]['permission'])
            if permission_num <= 10:
                continue

            card_num = len(process_info)
            """
            normal
            """
            if card_num <= soft_max_card_num:
                middle_user_dict[user] = {'count': 0, 'card_num': card_num}
                continue

            """
            middle
            """
            if card_num <= hard_max_card_num:
                if user not in middle_user_dict:
                    middle_user_dict[user] = {'count': 1, 'card_num': card_num}
                else:
                    middle_user_dict[user]['count'] += 1
                    middle_user_dict[user]['card_num'] = card_num

                sorted_card_info_list = get_sorted_card_info_list(process_info)
                for card_info in sorted_card_info_list[soft_max_card_num:]:
                    for p_info in card_info:
                        if p_info['runtime'] > soft_time:
                            kill_process_by_p_info(p_info, history_p_info_dict)
                continue

            """
            hard
            """
            if user not in middle_user_dict:
                middle_user_dict[user] = {'count': 1, 'card_num': card_num}
            else:
                middle_user_dict[user]['count'] += 1
                middle_user_dict[user]['card_num'] = card_num

            sorted_card_info_list = get_sorted_card_info_list(process_info)
            for card_info in sorted_card_info_list[hard_max_card_num:]:
                for p_info in card_info:
                    kill_process_by_p_info(p_info, history_p_info_dict)

        """
        send email
        """
        for user_info in user_info_list:
            uname = user_info['username']
            if uname in middle_user_dict and middle_user_dict[uname]['count'] == 1:
                send_email(user_info, middle_user_dict[uname]['card_num'], soft_max_card_num, hard_max_card_num, soft_time)


if __name__ == '__main__':
    main()
