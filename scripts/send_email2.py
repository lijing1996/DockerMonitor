# -*- coding: utf-8 -*-
# @Time    : 2018/9/9 6:24 PM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys
sys.path.append('./')

import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from db.db_manager import DatabaseManager
from config import mail_host, mail_user, mail_pass


def send_email(receiver, username, password, port, admin_open_port, node_name_list):
    sender = 'piaozhx@shanghaitech.edu.cn'
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_content = '''
    AI集群(10.19.124.11)将于周五周六(2018年9月28日, 29日)停机维护, 请保存好自己的数据并及时下线.

    请注意, 还没有迁移数据的, 请尽快将数据复制到/root之下(请不要复制无用的数据, 很多同学在AI集群中堆积了大量无用的模型数据, 集群80T的存储已经使用75T了).
    2018年10月10日 将删除所有/home下的数据.
    '''

    message = MIMEText(mail_content, 'plain', 'utf-8')
    message['From'] = Header("AI集群管理", 'utf-8')
    message['To'] = Header("AI集群用户", 'utf-8')

    message['Subject'] = Header('AI集群管理系统升级', 'utf-8')

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
        return False


def main():
    db = DatabaseManager()
    user_info_list = db.get_all_user_info()

    count = 0
    for user_info in user_info_list:
        username = user_info['username']
        receiver = user_info['email']
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']

        if receiver == 'test':
            continue

        node_name_list = [p['name'] for p in user_info['permission']]
        success = send_email(receiver, username, 'plus', container_port, open_port_range, node_name_list)

        while not success:
            # count = 0
            time.sleep(10)
            success = send_email(receiver, username, 'plus', container_port, open_port_range, node_name_list)

        # count += 1
        #
        # if count == 5:
        #     count = 0
        #     time.sleep(10)


if __name__ == '__main__':
    main()
