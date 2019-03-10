from django.db import models

# Create your models here.
import django.utils.timezone as timezone
# from DjangoUeditor.models import UEditorField


class UserMessage(models.Model):
	name = models.CharField(max_length=20, verbose_name="用户名")
	email = models.EmailField(verbose_name="邮箱")
	address = models.CharField(max_length=100, verbose_name="地址")
	message = models.TextField(verbose_name="留言内容")
	# message =  UEditorField(verbose_name="留言内容", width=1000, height=600,
	# 	# 			 imagePath="msg_ups/ueditor/",
	# 	# 			 filePath="msg_ups/ueditor/",
				 # blank=True, toolbars="full", default='')
	create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")


	def  __str__(self):
		return self.name


	class  Meta:
		db_table = "user_message"
		verbose_name = "用户留言"
		verbose_name_plural = verbose_name
		ordering = ["-create_time"]
