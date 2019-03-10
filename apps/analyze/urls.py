
from django.conf.urls import url
from analyze import views

urlpatterns = [
	url(r'^index/$', views.IndexHandler,name='index'),
	url(r'^art/', views.AnalyzeArtHandler,name='analyze_art'),
	url(r'^order/', views.AnalyzeOrderHandler,name='analyze_order'),
]
