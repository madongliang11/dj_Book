# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/10 下午2:19'
from django.contrib import messages
from django.shortcuts import HttpResponse, HttpResponseRedirect
from functools import wraps
from dj_Book.settings import R
import time, random
'''
django后台向前端发送一个闪现消息
利用django自带的message系统发送一个闪现消息
'''
def flash(request, title, text, level='info'):
   LEVEL_MAP = {
      'info':messages.INFO,
      'debug':messages.DEBUG,
      'success':messages.SUCCESS,
      'warning':messages.WARNING,
      'error':messages.ERROR
   }
   level = LEVEL_MAP[level]
   messages.add_message(request, level, text, title)
   return HttpResponse(text)


'''
校验用户是否登录，session是否有数据
校验成功，让之走正常逻辑，否则拒绝

@check_user_login
def index(request):
    pass
'''

def check_user_login(func):
   @wraps(func)
   def __wrapper(*args, **kwargs):
      #args = (request, )
      request = args[0]
      if not request.session.has_key("muser"):
         return HttpResponseRedirect("/user/login")
      return func(*args, **kwargs)
   return __wrapper


'''
保存redis key-value string数据
'''
def store_rds_str(key, value):
   try:
      R.set(key, value)
      return True
   except Exception as e:
      print(f"store_rds_str has error with {key}, {value}")
      return False


'''
产生订单号
'''
def create_order_id():
   order_id = "%s%s" % (int(time.time()), random.randint(10, 100))
   return int(order_id)

