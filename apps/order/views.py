from alipay import AliPay
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.cart.models import LineItem,Cart,OrderItemRelation
from apps.order.models import OrderItem,ProductOrder
from apps.book.models import Art
from dj_Book import settings
from dj_Book.utils import check_user_login, flash, create_order_id
from apps.order import forms
from django.views.decorators.csrf import csrf_exempt

'''
订单功能
'''
@check_user_login
def CartOrderHandler(request):
	user = request.session.get("muser")
	# 从购物车表中获取商品信息
	(total_price, product_list) = Cart.get_products(user)
	# 获取已经写好的订单表单
	order_form = forms.OrderForms()

	context = dict(
		user = user,
		total_price = total_price,
		product_list = product_list,
		form = order_form,
	)
	return render(request, "submit_order.html", context=context)


'''
提交订单功能
'''
@csrf_exempt
@check_user_login
def OrderSubmitHandler(request):
	url = request.path
	print(f"OrderSubmitHandler submit ok {url}")
	if request.method == "POST":
		order_form = forms.OrderForms(data=request.POST)
		if not order_form.is_valid():
			flash(request, "error", f"用户提交订单失败！")
			return CartOrderHandler(request)
		# cleaned_data中的值类型与字段定义的Field类型一致
		address = order_form.cleaned_data.get("address")
		pay_type = int(order_form.cleaned_data.get("pay_type"))
		phone = int(order_form.cleaned_data.get("phone"))
		order_id = create_order_id()
		user = request.session.get("muser")

		prod_order = ProductOrder(order_id=order_id, address=address, pay_type=pay_type, phone=phone,user_id=user.id)
		prod_order.save()

		# 得到当前用户的购物车的商品信息
		line_items = LineItem.objects.filter(Q(user=user.id) & Q(flag=0))
		# 将订单购物车关系表持久化
		[OrderItemRelation(line_item_id=int(line_item.id), product_order_id=prod_order.id).save()  for  line_item  in  line_items]
		# 将订单的商品持久化
		order = ProductOrder.objects.filter(order_id=order_id).first()
		[OrderItem(quantity=line_item.quantity,order_id=order.id,product_id=line_item.product_id,user_id=user.id).save() for line_item  in  line_items ]

		flash(request, "success", f"用户提交订单成功!,订单号为:{order_id}")

		"""开始支付"""
		amount = request.POST.get('amount')
		trad_no = order_id
		alipay = AliPay(
			appid=settings.APP_ID,
			app_notify_url='http://127.0.0.1/pay/notify/',
			app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
			alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
			sign_type='RSA2',
			debug=True
		)
		# 生成订单参数
		# 电脑网站的支付地址  https://openapi.alipaydev.com/gateway.do?order_url
		order_url = alipay.api_alipay_trade_page_pay(
			subject='爱尚书城订单',
			out_trade_no=trad_no,
			total_amount=amount,
			return_url='https://127.0.0.1/',  # 支付成功后前端跳转的网址
			notify_url='后台接收支付宝支付相关信息的接口 post请求'
		)
		pay_url = settings.ALT_PAY_DEV_URL + order_url
		return redirect(pay_url)

	return CartOrderHandler(request)





'''
查看订单功能
'''
@csrf_exempt
@check_user_login
def OrderViewHandler(request):
	user = request.session.get("muser")
	uid = user.id
	orders = ProductOrder.objects.order_by('-order_time').filter(Q(user_id=uid) & Q(flag=0))
	for order in orders:
		order.items = OrderItem.objects.filter(order_id=order.id)
		order.price = 0
		for order.item in order.items:
			order.item.art =  Art.objects.filter(id=order.item.product_id).first()
			order.item.price = int(order.item.art.a_price) * int(order.item.quantity)
			order.price += order.item.price

	context = {
		'orders':orders,
		'user':user
	}
	return render(request, 'view_order.html', context)

'''
删除订单功能
'''
@csrf_exempt
@check_user_login
def OrderHideHandler(request):
	oid = request.GET.get('oid')
	productorder = ProductOrder.objects.filter(id=oid).first()
	productorder.flag = 1
	productorder.save()

	return redirect(reverse('order:view_order'))

"""子表查询母表(多--->>>1)"""
# 写法1:子表对象.母表表名的小写.母表字段名
# products = line_item.art.objects.all()
# 写法2:子表名小写__子表字段="xxx"
# products = Art.objects.get(lineitem__orderitemrelation__product_order_id='')

"""母表查询子表(1--->>>多)"""
# # 写法1：子表小写_set的写法
# Art.objects.get(t_id='').art_content_set.all()
# # 写法2(推荐)： 写法：filter(子表外键字段__母表字段='过滤条件')
# Art.objects.filter(lineitem__orderitemrelation__product_order_id='')
# # 写法3:(原始写法,不推荐)
# art_id = Art.objects.get(t_id='').id
