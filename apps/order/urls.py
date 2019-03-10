from django.conf.urls import url
from apps.order import views

urlpatterns = [
	url(r'^cart/order/$', views.CartOrderHandler,name='cart_order'),
	url(r'^cart/submit_order/$', views.OrderSubmitHandler, name="submit_order"),
	url(r'^cart/view_order/$', views.OrderViewHandler, name="view_order"),
	url(r'^cart/hide_order/$', views.OrderHideHandler, name="hide_order"),
]