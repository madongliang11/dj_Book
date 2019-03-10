# -*- coding: utf-8 -*-
from apps.comment.models import Comment
from rest_framework import serializers
from apps.user.models import ArtsUser
from apps.book.models import Tag,Art,Content,Chapter


'''
序列化
类似于form
form                 serializer
html模板页面           api动态数据
'''

class ArtsUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtsUser
		fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'


class ArtSerializer(serializers.ModelSerializer):
	operator = serializers.ReadOnlyField(source="operator.username")

	class Meta:
		model = Art
		fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chapter
		fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'



