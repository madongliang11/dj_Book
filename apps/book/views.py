import random

from django.core.paginator import Paginator
from django.http import HttpResponse

from dj_Book import utils
from dj_Book.settings import logger
from apps.book import models
from apps.comment import forms
from apps.comment.models import Comment
from apps.book.models import Tag,Art

'''
首页卡片式页面展示：
      接口URL：  /book/index?page=1&t=1
     Models层中类的定义也属于接口范围
     方法：GET
      输入参数说明：
          page:   第几页
          t:  标签类别，整数标识  eg: 0--全部   1--爱情小说  2—科幻小说
      输出：
            渲染首页卡片式页面
'''

'''
	arts = Art.objects.all()
	for art in arts:
		tag = art.t_id.t_name
		art.tag = tag
		art.save()
	return HttpResponse('修改成功')
'''

def IndexHandler(request):
	logger.debug("IndexHandler:enter.")
	url = request.path
	t = int(request.GET.get('t', 0))
	page = int(request.GET.get('page', 1))
	tags = models.Tag.objects.filter(t_flag = 0)  #获取未删除的标签
	if t == 0:
		total = models.Art.objects.filter(a_flag = 0).count()
	else:
		total = models.Art.objects.filter(a_flag=0, t_id=t).count()
	# logger.info(f"IndexHandler, t:{t}, page:{page}, total:{total}")
	context = dict(
		pagenum = 1,
		total = 0,
		prev = 1,
		next = 1,
		pagerange = range(1, 2),
		data = [],
		url = url,
		tags = tags,
		page = page,
		t = t,
	)
	shownum = 12
	if total > 0:
		import math
		pagenum = int(math.ceil(total / shownum))
		#logger.warn(f"IndexHandler, pagenum: {pagenum}")
		if page < 1:
			url = url + "?page=1&t=%d" % t
			return HttpResponseRedirect(url)
		if page > pagenum:
			url = url + "?page=%d&t=%d" % (pagenum, t)
			return HttpResponseRedirect(url)
		offset = (page - 1) * shownum
		if t == 0:
			data = models.Art.objects.filter(a_flag=0)[offset:offset + shownum]
		else:
			data = models.Art.objects.filter(t_id=t, a_flag=0)[offset:offset + shownum]
		key = "page:%d:t:%d" % (page, t)

		utils.store_rds_str(key, data)

		btnum = 5
		if btnum > pagenum:
			firtpage = 1
			lastpage = btnum
		else:
			if page == 1:
				firtpage = 1
				lastpage = btnum
			else:
				firtpage = page - 2
				lastpage = page + btnum - 2
				if firtpage < 1:
					firtpage = 1
				if lastpage > pagenum:
					lastpage = pagenum
		prev = page - 1
		next = page + 1
		if prev < 1:
			prev = 1
		if next > pagenum:
			next = pagenum

		context = dict(
			pagenum=pagenum,
			total=total,
			prev=prev,
			next=next,
			pagerange=range(firtpage, lastpage + 1),
			data=data,
			url=url,
			tags=tags,
			page=page,
			t=t,
		)
	print(context)
	return render(request, "book_index.html", context=context)
	#return HttpResponse("主页面")


'''
详情页面功能：
       接口URL：  /book/detail?id=7
      方法：GET
      输入参数说明：
          id： 文章id，（点击某一个具体的文章，传入文章id)
     输出：
          渲染详情页面
'''

def DetailHandler(request):
	a_id = int(request.GET.get("id", 0))
	if a_id == 0:
		return HttpResponseRedirect("/book/index")
	#获取小说详情
	art_queryset = models.Art.objects.get(id = a_id)

	#获取小说对应的章节
	art_capters = models.Chapter.objects.filter(a_id=a_id)

	#获取评论表单
	comment_form = forms.CommentForm()
	comment_list = Comment.objects.filter(art_id = a_id)
	context = dict(
		art = art_queryset,
		art_capters = art_capters,
		form = comment_form,
		comment_list = comment_list,
		comment_count = comment_list.count(),
	)

	return render(request, "book_detail.html", context=context)


'''
小说章节
/book/capter?id=capter_id
'''
def ArtCapterHandler(request):
	capter_id = int(request.GET.get("id", 0))
	if capter_id == 0:
		return  DetailHandler(request)
	art_capter = models.Chapter.objects.get(id = capter_id)
	context = dict(
		art_capter = art_capter
	)
	return render(request, "book_captcha.html", context=context)


from django.shortcuts import render, HttpResponseRedirect
from .models import Tag, Art
from django.db.models import Q

'''
页面分类功能：
'''
def ClassifyHandler(request):

	arts = Art.objects.all()
	arts_count = arts.count()
	# 获取所有的标签
	tags = Tag.objects.filter(t_flag=0)
	tid = '0'
	hot= None
	price = None
	time = None

	# 根据标签进行筛选
	tid = request.GET.get('tid','0')
	if tid != '0':
		arts = arts.filter(t_id=tid)
		arts_count = arts.count()

	# 1 升序  0 降序
	# 根据热度进行筛选
	hot = request.GET.get('hot')
	a = type(hot)
	if hot == '1':
		arts = arts.order_by('hot')
	elif hot == '0':
		arts = arts.order_by('-hot')

	# 根据价格进行筛选
	# 排序
	price = request.GET.get('price')
	if price == '1':
		arts = arts.order_by('a_price')
	elif price == '0':
		arts = arts.order_by('-a_price')

	# 价格
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	if min_price and max_price:
		arts = arts.filter(a_price__range=[int(min_price),int(max_price)])
		arts_count = arts.count()



	# 根据时间进行筛选
	time = request.GET.get('time')
	if time == '1':
		arts = arts.order_by('a_createtime')
	elif time == '0':
		arts = arts.order_by('-a_createtime')


	"""分页"""
	paginator = Paginator(arts, 12)
	page = request.GET.get('page')
	if page:
		page = int(page)
	else:
		page = 1
	if page > paginator.num_pages:
		page = 1
	arts_page = paginator.page(page)
	num_pages = paginator.num_pages
	if num_pages < 5:
		# 1-num_pages
		pages = range(1, num_pages + 1)
	elif page <= 3:
		pages = range(1, 6)
	elif num_pages - page <= 2:
		# num_pages-4, num_pages
		pages = range(num_pages - 4, num_pages + 1)
	else:
		# page-2, page+2
		pages = range(page - 2, page + 3)

	# 组织模板数据
	context = {
		'tags': tags,
		'pages': pages,
		'arts_page': arts_page,
		'arts_count':arts_count,
		'tid':tid,
		'hot':hot,
		'price':price,
		'time':time
	}
	return render(request, "book_classify.html", context=context)

def RecommendHandler(request):
	pass
