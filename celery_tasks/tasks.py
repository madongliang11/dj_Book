from django.conf import settings
from django.core.mail import send_mail


import os
import sys
sys.path.insert(0, './')
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_Book.settings")
django.setup()

# 导入Celery类
# from celery import Celery

# 创建一个Celery类的对象
# app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/11')
from celery_tasks.celery import app

# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件内容
    subject = '爱尚书城欢迎你'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = "<h1>%s, 欢迎您成为python1804的一员</h1>请点击以下链接激活您的账户(7个小时内有效)<br/><a href='http://127.0.0.1:9000/user/activate?token=%s'>http://127.0.0.1:9000/user/activate?token=%s</a>" % (username, token, token)

    # 发送激活邮件
    # send_mail(subject=邮件标题, message=邮件正文,from_email=发件人, recipient_list=收件人列表)
    send_mail(subject, message, sender, receiver, html_message=html_message)









