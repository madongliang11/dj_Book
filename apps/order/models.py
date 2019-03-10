from django.db import models
from django.utils import timezone
from dj_Book.settings import  PAY_CHOICES
from apps.book.models import Art
# from DjangoUeditor.models import UEditorField
from apps.user.models import ArtsUser

'''
订单数据模型
'''
class ProductOrder(models.Model):
	order_id = models.BigIntegerField(verbose_name="订单号", unique=True)
	pay_type = models.IntegerField(default=0, verbose_name="支付类型", choices=PAY_CHOICES)
	address = models.CharField(default='', max_length=200, verbose_name="订单配送地址")
	phone = models.BigIntegerField(default=0, verbose_name="联系方式")
	order_time = models.DateTimeField(default=timezone.now, db_index=True,verbose_name="下单时间")
	user = models.ForeignKey(ArtsUser,verbose_name="用户")
	flag = models.IntegerField(verbose_name="是否隐藏",default=0)

	def __str__(self):
		return self.order_id


	class Meta:
		db_table = "product_order"
		verbose_name = "用户订单"
		verbose_name_plural = verbose_name


class OrderItem(models.Model):
	order = models.ForeignKey(ProductOrder,verbose_name='订单号')
	product = models.ForeignKey(Art,verbose_name='商品编号')
	user = models.ForeignKey(ArtsUser, verbose_name="购买用户")
	quantity =  models.CharField(max_length=10)

	class Meta:
		db_table = "order_item"
		verbose_name = "订单商品"
		verbose_name_plural = verbose_name


