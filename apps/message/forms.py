# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '202018/6/22 上午9:07'

from django import forms

from django.forms import widgets
from apps.message import models

from django.core.exceptions import  ValidationError

class UserMessageForm(forms.Form):
	name = forms.CharField(
		     label = "用户名",
			 required = True,
		     min_length = 5,
		     max_length = 20,
		     #<input type="text" class="form-control" />
			 widget = widgets.TextInput(attrs={
				 "class":"form-control",
				 "placeholder":"请输入您的姓名, 长度为5~20",
			 }),
		     error_messages = {
				 "required":"用户名不能为空",
				 "min_length":"不行, 长度小于5",
				 "max_length":"sorry, 长度太长，超过20",
			 })
	email = forms.EmailField(
		     label="邮箱",
		     required = True,
			 widget = widgets.TextInput(attrs={
				 "placeholder":"请输入邮箱",
			      }),
		     error_messages = {
				 "required":"邮箱不能为空！",
				 "invalid":"抱歉，请输入合法的邮箱！",
			 }
	        )
	address = forms.CharField(
		     label = "地址",
		     widget = widgets.TextInput(attrs={"placeholder":"请输入地址"}),
		     max_length = 200,
			)
	message = forms.CharField(
             label = "留言",
		     widget = widgets.Textarea(attrs={"placeholder":"请输入用户留言信息"})
			)


	def clean_name(self):
		#对name字段进行扩展校验，在models层进行db是否存在校验
		name = self.cleaned_data.get("name")
		users = models.UserMessage.objects.filter(name = name).count()
		if users:
			raise  ValidationError("用户已存在！")
		return name


	def clean_email(self):
		email = self.cleaned_data.get("email")
		users = models.UserMessage.objects.filter(email=email).count()
		if users:
			raise ValidationError("邮箱已存在！")
		return email
