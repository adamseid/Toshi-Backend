"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from toshi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/toshi/assets/$', views.assetRequest),
    re_path(r'^api/toshi/walletBalance/$', views.walletBalanceRequest),
    re_path(r'^api/toshi/graph/$', views.graphRequest),
    re_path(r'^api/toshi/accountGraph/$', views.accountGraphRequest),
    re_path(r'^api/toshi/account/$', views.account),
    re_path(r'^api/toshi/accounthistory/$', views.accounthistory),
    re_path(r'^api/toshi/$', views.httpRequest),
    re_path(r'^api/toshi/volume_history_overview', views.volume_history_overview),
    re_path(r'^api/toshi/history', views.history),
]
