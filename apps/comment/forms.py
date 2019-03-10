# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/11 上午10:48' 

'''
评论的表单
'''
from django import forms
from apps.comment.models import Comment

'''
用户评论的form表单
'''
class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['name', 'title', 'text']





