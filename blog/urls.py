"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from apps.users.views import LoginView

from rest_framework import permissions



urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('apps.users.urls')),
    path('post/', include('apps.posts.urls.urlspost')),
    path('likes/',include('apps.posts.urls.urlslike')),
    path('comments/',include('apps.posts.urls.urlscomment')),
    path('permissions/',include('apps.permissions.urls.urlspermission')),
    path('categories/',include('apps.permissions.urls.urlscategory')),
    path('',LoginView),

]
