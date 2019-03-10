from django.conf.urls import url
from apps.user import views

urlpatterns = [
    url(r"^register/$", views.RegisterHandler, name="register"),
	url(r"^login/$", views.LoginHandler, name="login"),
	url(r'^logout/$', views.LogoutHandler,name="logout"),
	url(r'^activate/$', views.ActivateHandler,name="activate"),
]
