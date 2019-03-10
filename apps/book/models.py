from django.db import models
import django.utils.timezone as timezone
from dj_Book.settings import  DB_FIELD_VALID_CHOICES
from DjangoUeditor.models import UEditorField
import time, datetime

'''
小说标签类
'''
class Tag(models.Model):
	id = models.CharField(primary_key=True,max_length=20)
	t_name = models.CharField(max_length=20, verbose_name="文章标签")
	t_url = models.CharField(max_length=255,verbose_name="标签链接")
	t_createtime = models.DateTimeField(default=timezone.now,  db_index=True, verbose_name="创建时间")
	#t_createtime = models.IntegerField(default=datetime.datetime.now(),  verbose_name="创建时间")
	t_flag = models.IntegerField(default=0, verbose_name="控制字段", choices=DB_FIELD_VALID_CHOICES)

	def __str__(self):
		return self.t_name

	class  Meta:
		verbose_name = "标签"
		verbose_name_plural = verbose_name
		db_table = "tag"
		ordering = ["-t_createtime"]    #按照创建时间降序

'''
小说介绍信息
'''
class Art(models.Model):
	id = models.CharField(primary_key=True,max_length=20)
	tag = models.CharField(max_length=20, null=True)
	a_title = models.CharField(max_length=100, verbose_name="文章标题")
	a_info = models.CharField(max_length=200, verbose_name="文章描述")
	a_author = models.CharField(max_length=50,verbose_name="文章作者")
	a_img_url = models.CharField(max_length=255)
	a_img_url_figer = models.CharField(max_length=255)
	a_content_ue = UEditorField(verbose_name="文章内容", width=800, height=400,
							 imagePath="media/arts_ups/ueditor/",
							 filePath="media/arts_ups/ueditor/",
							 blank=True, null=True, toolbars="full", default='')
	a_createtime = models.DateTimeField(default=timezone.now, db_index=True,verbose_name="添加时间")
	#a_createtime = models.IntegerField(default=int(time.time()),  verbose_name="添加时间")
	t_id = models.ForeignKey(Tag, verbose_name="关联文章标签",db_column='t_id')
	a_price = models.IntegerField(default=0, null=True, verbose_name="单价")
	a_flag = models.IntegerField(default=0,  verbose_name="控制字段", choices=DB_FIELD_VALID_CHOICES)
	operator = models.ForeignKey("auth.User", default=1, verbose_name="api操作者",db_column='operator',null=True)
	hot = models.IntegerField(default=0,verbose_name="热度", null=True)


	def __str__(self):
		return self.a_title


	class Meta:
		verbose_name = "小说"
		verbose_name_plural = verbose_name
		db_table = "art"
		ordering = ["-a_createtime"]  # 按照创建时间降序


'''
小说的内容信息
'''
class Content(models.Model):
	id = models.CharField(primary_key=True, max_length=20)
	a_content = models.TextField(verbose_name="小说内容",null=True)
	a_id = models.ForeignKey(Art, verbose_name="小说", db_column='a_id')
	class Meta:
		db_table = "art_content"
		verbose_name = "小说内容"
		verbose_name_plural = verbose_name

'''
小说的章节信息
'''
class Chapter(models.Model):
	id = models.CharField(primary_key=True,max_length=20)
	a_id = models.ForeignKey(Art, verbose_name="小说",db_column='a_id')
	title = models.CharField(max_length=100, verbose_name="章节标题")
	content = models.TextField(verbose_name="小说章节内容",null=True)
	create_time = models.DateTimeField(default=timezone.now, db_index=True,verbose_name="添加时间")
	#create_time = models.IntegerField(default=int(time.time()), db_index=True, verbose_name="添加时间")

	class Meta:
		db_table = "art_chapter"
		verbose_name = "小说章节"
		verbose_name_plural = verbose_name











