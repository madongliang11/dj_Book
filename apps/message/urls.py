from django.conf.urls import url
from apps.message import views


urlpatterns = [
	url(r"^$", views.MessageSubmitHandlerV2, name="form"),
]