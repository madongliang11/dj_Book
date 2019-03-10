from django.conf.urls import url
from apps.book import views
from apps.book.test import test_param

urlpatterns = [
	url(r"^index/$", views.IndexHandler,name='index'),
	url(r'^classify/$', views.ClassifyHandler,name='classify'),
	url(r'^detail/$', views.DetailHandler,name='detail'),
	url(r'^capter/$', views.ArtCapterHandler,name='capter'),
	url(r'^test_param/(?P<art_pk>[0-9]+)/$', test_param, name="param"),
]