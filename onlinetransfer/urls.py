"""onlinetransfer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from online import views
from onlinetransfer.settings import MEDIA_ROOT
from django.views.static import  serve
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getpreImage/', views.getPreImage, name='getPreImage'),
    url(r'^getprocessedImage/', views.getProcessedImage, name='getProcessedImage'),
    url(r'^index/', views.index, name='index'),
    url(r'^getVideoPoster/', views.getVideoPost, name='getVideoposter'),
    url(r'^getProgress/', views.getProgress, name='getProgress'),
    url(r'^$', views.home, name='home'),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
