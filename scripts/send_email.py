# -*- coding: utf-8 -*-
# @Time    : 2018/9/9 6:24 PM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

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
    由于学校邮件服务器有奇怪问题, 故重新发送一遍, 已收到的同学可以无视.
    
    AI集群新管理系统已上线完毕, 由于新集群使用方法和原来差别很大, 故请大家一定要看AI集群文档(http://10.19.124.11:8898/).

    请大家一定要看AI集群文档(http://10.19.124.11:8898/)!!!
    请大家一定要看AI集群文档(http://10.19.124.11:8898/)!!!
    请大家一定要看AI集群文档(http://10.19.124.11:8898/)!!!

    请注意, 你的旧数据存放在/home/username下面, 请尽快将数据复制到/root之下(请不要复制无用的数据, 很多同学在AI集群中堆积了大量无用的模型数据, 集群80T的存储已经使用75T了).
    一个月之后(2018年10月10日) 将删除所有/home下的数据.

    另外请注意AI集群的IP是10.19.124.11, 在填写表格的时候有部分同学提到的数据文件(请保留xxx/xxx等)我并没有在集群中找到, 有些同学可能把AI集群(10.19.124.11)和P40集群(10.15.22.198)搞混了.

    你在AI集群的新账号:
    username: %s
    password: %s
    port: %s
    admin_open_port: %s
    
    你申请的节点权限: 
    %s
    ''' % (username, password, port, admin_open_port, node_name_list)

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
        print("%s 邮件发送成功" % username)
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
