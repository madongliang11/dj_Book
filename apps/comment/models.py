from django.db import models

# Create your models here.
from django.utils import timezone
from apps.book.models import Art
from dj_Book.settings import DB_FIELD_VALID_CHOICES
'''
评论模块数据模型
'''
class Comment(models.Model):
	name = models.CharField(max_length=50, verbose_name="评论者")
	title = models.CharField(max_length=200, verbose_name="评论标题")
	text = models.TextField(verbose_name="评论内容")
	created_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="创建时间")
	art = models.ForeignKey(Art, verbose_name="关联的小说")
	flag = models.IntegerField(default=0, verbose_name="控制字段", choices=DB_FIELD_VALID_CHOICES)


	def __str__(self):
		return self.title

	class Meta:
		db_table = "comments"
		verbose_name = "用户评论"
		verbose_name_plural = verbose_name
		ordering = ["-created_time"]

