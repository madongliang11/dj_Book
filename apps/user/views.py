from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from apps.user import forms
from apps.user import models
from django.views.decorators.csrf import csrf_exempt

from dj_Book import settings
from dj_Book.utils import flash
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

'''
加密算法：
可逆加密算法：BASE-64
不可逆加密算法: MD5
'''

'''
会员注册功能
支持方法：
GET --- 获取空注册表单
POST --- 提交注册表单
表单：forms.ArtsUserRegForm
数据模型:models.ArtsUser
'''
def create_pwd_md5(str_password):
	import hashlib
	h1 = hashlib.md5()
	h1.update(str_password.encode(encoding="utf-8"))
	return h1.hexdigest()


@csrf_exempt
def RegisterHandler(request):
	reg_form = forms.ArtsUserRegForm()
	method = request.method
	if method == "POST":
		reg_form = forms.ArtsUserRegForm(data=request.POST)
		if not reg_form.is_valid():
			#return HttpResponse("form is not valid")
			flash(request, "error", f"用户注册校验失败！")
			context = dict(form=forms.ArtsUserRegForm(data=request.POST))
			return render(request, "user_register.html", context=context)
		username = reg_form.cleaned_data.get("username")
		password = create_pwd_md5(reg_form.cleaned_data.get("password"))
		email = reg_form.cleaned_data.get("email")
		user = models.ArtsUser(username=username, password=password, email=email)
		user.save()
		flash(request, "success", f"恭喜，注册用户{username}成功！！")

		# 开始发送邮件(根据flag=0  : 表示未激活  flag=1  :  表示 激活)
		# 对用户的身份信息进行加密，生成激活token信息
		# serializer = Serializer('加解密密钥', '解密有效时间')
		serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
		info = {'confirm': user.id}
		# # 调用dumps方法实现加密，返回值类型为bytes
		token = serializer.dumps(info)
		# 将其转换为str
		token = token.decode()
		send_register_active_email.delay(email, username, token)

	context = dict(form = reg_form)

	return render(request, "user_register.html", context=context)


@csrf_exempt
def LoginHandler(request):
	login_form = forms.ArtsUserLoginForm()
	if request.method == "POST":
		login_form = forms.ArtsUserLoginForm(data = request.POST)
		if not login_form.is_valid():
			flash(request, "error", f"用户登录校验失败！")
			context = dict(form=forms.ArtsUserLoginForm())
			return render(request, "user_login.html", context=context)
		username = login_form.cleaned_data.get("username")
		password = create_pwd_md5(login_form.cleaned_data.get("password"))
		user = models.ArtsUser.objects.filter(username=username, password=password)
		user_first = user.first()
		if user_first:  #登录验证成功，用户名和密码都正确
			request.session["muser"] = user_first
			return HttpResponseRedirect("/book/index")
		flash(request, "error", f"用户{username}登录失败！")

	context = dict(form = login_form)
	return render(request, "user_login.html", context=context)


def LogoutHandler(request):
	del request.session["muser"]
	return redirect('/')


def ActivateHandler(request):
	"""激活"""
	serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
	try:
		token = request.GET.get('token')
		# # 调用loads方法实现解密
		info = serializer.loads(token)
		# 获取待激活用户id
		user_id = info['confirm']
		# 激活用户
		user = models.ArtsUser.objects.get(id=user_id)
		user.flag = 1
		user.save()

		# 跳转登录页面
		return redirect('/')
	except:
		# 激活链接已失效
		# 实际开发: 返回页面，让你点击链接再发激活邮件
		return HttpResponse('激活链接已失效')