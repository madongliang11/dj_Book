"""dj_Book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
import xadmin
from django.views.generic.base import RedirectView

from apps.order.pay_helper import pay

urlpatterns = [
    url('xadmin/', xadmin.site.urls),
    url(r'^$',  RedirectView.as_view(url="/book/index"),name='index'),
    url(r'^book/', include("book.urls",namespace='art')),
    url(r'^comment/', include("comment.urls",namespace='comment')),
    url(r'^message/', include("message.urls",namespace='message')),
    url(r'^order/', include("order.urls",namespace='order')),
    url(r'^cart/', include("cart.urls",namespace='cart')),
    url(r'^user/', include("user.urls",namespace='user')),
    url(r'^apis/', include("apis.urls")),
    url(r'^analyze/', include("analyze.urls",namespace='analyze')),
    url(r'^search/', include('haystack.urls',namespace='search')),
    url(r'^captcha', include('captcha.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls'))
]
