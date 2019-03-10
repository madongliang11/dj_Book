from django.conf.urls import url
from apps.cart import views

urlpatterns = [
    url(r'^cart/view/$', views.ViewCartHandler,name='view'),
	url(r'^cart/add/$', views.AddCartHandler,name='add'),
	url(r'^cart/sub/$', views.SubCartHandler,name='sub'),
	url(r'^cart/clean/$', views.CleanCartHandler,name='clean'),
]
