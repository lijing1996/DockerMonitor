# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 12:46 PM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys

sys.path.append('./')

import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from config import mail_host, mail_user, mail_pass


def send_email(chs_name, receiver, grade):
    sender = 'piaozhx@shanghaitech.edu.cn'
    receivers = [receiver]

    mail_content = '''
    Hi, %s:
    你的CS172课程最终成绩: %f, 如对自己的成绩有疑问, 请在三天内来核查.
    ''' % (chs_name, grade)

    message = MIMEText(mail_content, 'plain', 'utf-8')
    message['From'] = Header("CS172TA", 'utf-8')
    message['To'] = Header("CS172上课同学", 'utf-8')

    message['Subject'] = Header('CS172课程成绩', 'utf-8')

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
    with open('cs172_grade.txt', 'r') as f:
        student_info_list = f.readlines()
        student_info_list = map(lambda x: x.split(), student_info_list)

    for sid, sname, email, grade in student_info_list:
        grade = float(grade)
        print(sid, sname, email, grade)

        success = send_email(sname, email, grade)

        while not success:
            # count = 0
            time.sleep(10)
            success = send_email(sname, email, grade)

        # count += 1
        #
        # if count == 5:
        #     count = 0
        #     time.sleep(10)


if __name__ == '__main__':
    main()
