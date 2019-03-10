from django.conf.urls import url, include
from apps.comment import views

app_name = "comments"

urlpatterns = [
	url(r"^book/(?P<art_pk>[0-9]+)/$", views.art_comment, name="art_comm")
]