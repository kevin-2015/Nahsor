# -*- coding:utf-8 -*-
# import pymysql
# import json
# db_config = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'password': '123456',
#     'db': 'nahsor',
#     'charset': 'utf8mb4'
# }
# db = pymysql.connect(**db_config)
# cur = db.cursor()
# d_json = {}
# d_json = json.dumps(d_json)
# tsql = "insert into jsondata(data) values('{json}')"
# sql = tsql.format(json=pymysql.escape_string(d_json))
# print(sql)


import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
# 第三方 SMTP 服务
mail_host="smtp.163.com"  #设置服务器
mail_user="fenyukuang@163.com"    #用户名
mail_pass="jk201148"   #口令 
 
 
sender = 'fenyukuang@163.com'
receivers = ['fenyukuang@gmail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
 
try:
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException:
    print ("Error: 无法发送邮件")

