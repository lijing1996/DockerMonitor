# -*- coding: utf-8 -*-
# @Time    : 2018/10/6 22:47
# @Author  : Yongfei Liu
# @Email   : liuyf3@shanghaitech.edu.cn
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
    尊敬的AI-Courses集群用户%s: 
    
    AI-Courses-Cluster使用注意事项:
    
    1. 按照计划，为每位没有显卡资源的同学开通AI-Courses-Cluster的使用权限, 该GPU资源仅为课程作业以及课程project使用，切做其他用途。
    2. 由于资源有限，同一节点安排人数较多，请大家错峰使用，切勿恶意抢占资源。
    3. 有关集群使用方法: 请查看AI-Cluster使用文档(http://10.19.124.11:8898/).
    4. 考虑大家会用jupyter来写课程作业，AI-Courses-Cluster jupyter 配置方法请参考文档(http://10.19.124.11:8898/QA_container/).
    5. 大家所有程序需要进入节点运行，切勿在Admin运行。
    6. 该资源仅作上课时间使用，课程结束后15日内，我们会删除所有课程账号，请及时保存好自己的文件。
    
    
    用户信息小结:
    username: %s
    ssh port: %d
    admin_open_port: %s
    node list: %s

    admin登录方式以及进入节点:
    ssh root@10.19.124.11 -p %d
    ssh node13
    
    ''' % (chs_name, username, port, admin_open_port, str(node_name_list), port)

    message = MIMEText(mail_content, 'plain', 'utf-8')
    message['From'] = Header("AI-Courses集群管理", 'utf-8')
    message['To'] = Header("AI-Courses集群用户", 'utf-8')

    message['Subject'] = Header('AI-Courses集群权限开通', 'utf-8')

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

        if 'cs280' in username:

            node_name_list = [p['name'] for p in user_info['permission']]
            success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)
            while not success:
                # count = 0
                time.sleep(10)
                success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)

        #
        # if count == 5:
        #     count = 0
        #     time.sleep(10)


if __name__ == '__main__':
    main()