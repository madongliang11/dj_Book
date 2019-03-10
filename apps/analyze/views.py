from django.shortcuts import render
from dj_Book.utils import check_user_login
from apps.book.models import Tag,Art
from apps.order.models import OrderItem, ProductOrder
import json

@check_user_login
def IndexHandler(request):
    return render(request, "analyze_index.html")

from django.db.models import Count, Q


def AnalyzeArtHandler(request):
    tags = Tag.objects.filter(t_flag = 0).order_by('id')
    arts = Art.objects.all()
    nums = []
    hots = [1,2,3,4,5,6,7,8,9,10]

    for tag in tags:
        arts = tag.art_set.all()
        arts_num = arts.count()
        tag.arts_num = arts_num
        nums.append(arts_num)
        # 分组函数, 用于实现聚合groupby查询前面的values写的是谁，就group谁,通过计算得到的聚合值的字典
        tag.hot_nums = arts.order_by('hot').values('hot').annotate(hot_num=Count('id'))
        # 通过计算得到的聚合值的字典
        # users = Arts.aggregate(hot_num=Count('hot'))

    context = {
        'tags':tags,
        'nums':nums,
        'hot':hots
    }
    return render(request, "analyze_art.html",context=context)


def AnalyzeOrderHandler(request):
    user = request.session.get("muser")
    uid = user.id
    orders = ProductOrder.objects.order_by('-order_time').filter(user_id=uid)
    items = OrderItem.objects.all().distinct()
    for order in orders:
        order.items = OrderItem.objects.filter(order_id=order.id)
        order.price = 0
        for order.item in order.items:
            order.item.art = Art.objects.filter(id=order.item.product_id).first()
            order.item.price = int(order.item.art.a_price) * int(order.item.quantity)
            order.price += order.item.price



    context = {
        'orders': orders,
        'user': user,
        'items':items
    }
    return render(request, "analyze_order.html", context)

