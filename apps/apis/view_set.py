'''
使用视图集来进行逻辑处理
'''

from rest_framework import viewsets
from rest_framework import permissions
from apps.user.models import ArtsUser
from apps.book.models import Tag, Art,Content,Chapter
from apps.apis.permissions import IsOwnerOrReadOnly
from apps.comment.models import Comment
from apps.apis import serializers

"""基于类的视图的写法"""
class ArtsUserViewSet(viewsets.ModelViewSet):
	queryset = ArtsUser.objects.all()[0:9]
	serializer_class = serializers.ArtsUserSerializer
	permission_classes = (IsOwnerOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class =  serializers.TagSerializer
	permission_classes = (IsOwnerOrReadOnly,)


class ArtViewSet(viewsets.ModelViewSet):
	queryset = Art.objects.all()
	serializer_class =  serializers.ArtSerializer
	permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticatedOrReadOnly)


class ContentViewSet(viewsets.ModelViewSet):
	queryset = Content.objects.all()
	serializer_class = serializers.ContentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ChapterViewSet(viewsets.ModelViewSet):
	queryset = Chapter.objects.all()
	serializer_class = serializers.ChapterSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = serializers.CommentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
