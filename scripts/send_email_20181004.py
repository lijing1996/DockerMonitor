# -*- coding: utf-8 -*-
# @Time    : 2018/10/4 1:16 PM
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


def send_email(chs_name, receiver, username, password, port, admin_open_port, node_name_list):
    sender = 'piaozhx@shanghaitech.edu.cn'
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_content = '''
    尊敬的AI集群用户%s: 
    
    AI集群(10.19.124.11)已维护完成.

    更新内容:
    1. 机房迁移, 增加8台计算节点以及6台分布式存储节点
    2. 所有用户挂载224T分布式存储, 包括只读数据路径/datasets, 私人数据路径/p300
    3. 管理网站稳定性升级
    4. AI集群峰值测试
    5. 所有用户hostname 由 name.node 转为 name-node
    6. 所有用户容器网络模式由桥接模式转为共享模式

    请注意, 还没有迁移数据的, 请尽快将数据复制到/root之下(请不要复制无用的数据, 很多同学在AI集群中堆积了大量无用的模型数据, 集群80T的存储已经使用75T了).
    2018年10月10日 将删除所有/home下的数据.
    
    请注意, 还没有迁移数据的, 请尽快将数据复制到/root之下(请不要复制无用的数据, 很多同学在AI集群中堆积了大量无用的模型数据, 集群80T的存储已经使用75T了).
    2018年10月10日 将删除所有/home下的数据.
    
    请注意, 还没有迁移数据的, 请尽快将数据复制到/root之下(请不要复制无用的数据, 很多同学在AI集群中堆积了大量无用的模型数据, 集群80T的存储已经使用75T了).
    2018年10月10日 将删除所有/home下的数据.
    
    有部分同学没有理解上文中"迁移数据"是什么意思, 在这里在重复一遍, 你要做的是将/home/name下的有用数据拷贝到/root下, 到期之后你的容器中将不再有/home这个文件夹, 其中的文件也将会删除.
    
    用户信息小结:
    username: %s
    ssh port: %d
    admin_open_port: %s (已废弃)
    node list: %s
    
    admin登录方式:
    ssh root@10.19.124.11 -p %d
    
    ''' % (chs_name, username, port, admin_open_port, str(node_name_list), port)

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
        chs_name = user_info['chinese_name']
        receiver = user_info['email']
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']

        if receiver == 'test':
            continue

        if username not in ['piaozx']:
            continue

        node_name_list = [p['name'] for p in user_info['permission']]
        success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)

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
