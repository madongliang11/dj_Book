from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

from apps.book.models import  Art
from apps.cart.models import Cart,LineItem
from dj_Book.utils import check_user_login


'''
查看购物车
接口：/book/cart/view
'''
@check_user_login
def ViewCartHandler(request):
	user = request.session.get("muser")

	# 购物车选择操作 0 已选 1 未选择
	try:
		item_id = request.GET.get("item_id")
		item = LineItem.objects.filter(id=item_id).first()
		kind = request.GET.get("kind")
		if kind == '1':
			item.flag = 1
		elif kind == '0':
			item.flag = 0
		item.save()
	except Exception as e:
		pass

	# 获取购物车商品(包括选中和未选中的)并展示
	(total_price, product_list) =  Cart.get_products(user)
	context = dict(
		user = user,
		total_price = total_price,
		product_list = product_list,
	)
	return render(request, "view_cart.html", context=context)


'''
添加商品到购物车
接口：/book/cart/add?id=小说id
'''
@check_user_login
def AddCartHandler(request):
	art_id = int(request.GET.get("id", 0))
	quantity = int(request.GET.get("num",1))

	# 获取立即购买的商品
	now = request.GET.get("now")

	if art_id == 0:
		return HttpResponseRedirect("/book/index")
	product = Art.objects.get(id = art_id)
	user = request.session.get("muser")
	Cart.add_product(product, user,quantity)

	# 如果是立即购买(默认将购买的商品加至购物车,主要实现代码重用),直接调至订单页
	if now == "now":
		return redirect(reverse('order:submit_order'))

	return ViewCartHandler(request)


@check_user_login
def SubCartHandler(request):
	art_id = int(request.GET.get("id", 0))
	if art_id == 0:
		return HttpResponseRedirect("/book/index")
	product = Art.objects.get(id = art_id)
	user = request.session.get("muser")
	Cart.sub_product(product, user)
	return ViewCartHandler(request)


'''
清空购物车
'''
@check_user_login
def CleanCartHandler(request):
	#del request.session['cart']
	user = request.session.get("muser")
	item_id = request.GET.get('item_id')
	#line_items = LineItem.objects.filter(user=user.id)
	#删除用户对应的订单信息
	#[ProductOrder.objects.filter(order_id=item.product_order_id).delete()   for item in line_items]
	#删除购物车条目信息
	if item_id:
		LineItem.objects.filter(Q(user=user.id) & Q(id=item_id)).delete()
	else:
		LineItem.objects.filter(user=user.id).delete()
	return ViewCartHandler(request)

