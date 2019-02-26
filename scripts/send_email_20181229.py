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
    Hi, %s:
AI集群(10.19.124.11)将于2019年12月30日(周日)停机维护:
更新内容:
1. 解决部分用户在安装软件之后cuda mismatch的问题
2. 在admin添加motd, 提示不要在admin跑程序, 以及不要在/下创建文件夹以及存储文件, 添加doc链接
3. 将用户名由name_admin改为name-admin
4. 解决用户开启jupyter失败的问题
5. 将显卡驱动由396升级至410 (支持cuda10)

届时服务器将不定期重启数次, 请事先保存自己的数据

AI集群运维团队
    ''' % (chs_name)

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
    user_info_list = db.get_all_user_info() + db.get_cs280_user_info()

    count = 0
    for user_info in user_info_list:
        username = user_info['username']
        chs_name = user_info['chinese_name']
        receiver = user_info['email']
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']

        if receiver in ['test', 'test2', 'NA']:
            continue

        node_name_list = [p['name'] for p in user_info['permission']]
        success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)

        while not success:
            # count = 0
            time.sleep(10)
            success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)

        # count += 1
        #
        # if count == 5:
        #     count = 0
        #     time.sleep(10)


if __name__ == '__main__':
    main()
