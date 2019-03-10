# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
from django.forms import widgets
from apps.user import models
from django.core.exceptions import ValidationError

'''
会员信息注册表单
基于数据模型ArtsUser
用户注册的信息会保存到cleaned_data
'''
class ArtsUserRegForm(forms.Form):
	username = forms.CharField(
		label = "用户名",
		required = True,
		min_length = 1,
		max_length = 10,
		widget = widgets.TextInput(
			attrs = {
				"class":"form-control",
				"placeholder":"请输入用户名，长度为1 ~ 10",
			}),
		error_messages = {
			"required": "对不起，输入的用户名不能为空",
			"min_length":"不行, 长度小于1",
			"max_length":"sorry, 长度大于10",
		}
	)
	password = forms.CharField(
		label =  "密码",
		required = True,
		min_length = 1,
		max_length = 10,
		widget = widgets.PasswordInput(
			attrs={
				"class":"form-control",
				"placeholder":"请输入密码, 长度为1~10",
			}),
		error_messages={
			"required": "密码不能为空",
			"min_length": "不行, 长度小于1",
			"max_length": "sorry, 长度大于10",
		}
	)
	email = forms.EmailField(
		label = "邮箱",
		required=True,
		widget=widgets.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "请输入邮箱",
			}),
		error_messages={
			"required": "邮箱不能为空",
		}
	)
	captcha = CaptchaField(label='验证码')


	def clean_username(self):
		#对会员信息的用户名username进行校验
		#此函数返回的结果会存到 cleaned_data
		username = self.cleaned_data.get("username", "")
		user_count = models.ArtsUser.objects.filter(username=username).count()
		if user_count:
			raise ValidationError("用户名已经存在！")
		return username



	def clean_email(self):
		#对会员信息的用户名username进行校验
		#此函数返回的结果会存到 cleaned_data
		email = self.cleaned_data.get("email", "")
		user_count = models.ArtsUser.objects.filter(email=email).count()
		if user_count:
			raise ValidationError("邮箱已经存在！")
		return email



'''
会员登录表单
'''
class ArtsUserLoginForm(forms.Form):
	username = forms.CharField(
		label="用户名",
		required=True,
		min_length=1,
		max_length=10,
		widget=widgets.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "请输入用户名，长度为1 ~ 10",
			}),
		error_messages={
			"required": "对不起，输入的用户名不能为空",
			"min_length": "不行, 长度小于1",
			"max_length": "sorry, 长度大于10",
		}
	)
	password = forms.CharField(
		label="密码",
		required=True,
		min_length=1,
		max_length=10,
		widget=widgets.PasswordInput(
			attrs={
				"class": "form-control",
				"placeholder": "请输入密码, 长度为1~10",
			}),
		error_messages={
			"required": "密码不能为空",
			"min_length": "不行, 长度小于1",
			"max_length": "sorry, 长度大于10",
		}
	)
	captcha = CaptchaField(label='验证码')

