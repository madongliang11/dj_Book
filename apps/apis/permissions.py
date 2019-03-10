# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/12 下午4:24' 

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	'''
	自定义权限功能，只允许对象的所有者编辑它
	'''
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.operator == request.user