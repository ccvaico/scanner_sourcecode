"""ScanDocker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('index', views.index),
    path('aboutus', views.aboutus),
    path('services', views.services),
    path('scanner', views.scanner),
    path('scannerscan', views.scanner_scan),
    path('scannerforms', views.scanner_forms),
    path('scannercharts', views.scanner_charts),
    path('scannertables', views.scanner_tables),
    path('knowledgegraph', views.knowledgegraph),
    path('blogitem', views.blogitem),
    path('pricing', views.pricing),
    path('blog', views.blog),
    path('contact', views.contact),
    path('test', views.test),
]

# 确保设置DEBUG为False时样式显示正常
if not settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
    ]