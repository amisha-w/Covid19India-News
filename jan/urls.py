"""jan URL Configuration

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
from django.contrib import admin
from django.urls import path
from newsapp import views

urlpatterns = [
    path('index/<coun>/',views.index, name='index'),
    path('index/<coun>/<keyw>/',views.index, name='index'),
    path('index/',views.index, name='index'),
    path('index/<keyw>/',views.index, name='index'),
    path('search/',views.search, name='search'),
    path('map/',views.map, name='map'),
    path('help/',views.help, name='help'),
    path('help/<c_id>/',views.help, name='help'),
    path('help/<c_id>/<s_id>/',views.help, name='help'),
    path('trend/',views.trend, name='trend'),
    path('trend/<tr>/',views.trend, name='trend'),
    path('top/',views.top, name='top'),
    path('top/<timey>/',views.top, name='top'),
    path('top/<timey>/<coun>/<sour>/',views.top, name='top'),
    path('top/<timey>/<coun>/',views.top, name='top'),
     path('', views.index, name ='index'), 
    path('admin/', admin.site.urls), 
]
