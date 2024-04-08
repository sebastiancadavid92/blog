from rest_framework.routers import DefaultRouter

from apps.users.views import login_view,logout_view


from django.urls import path

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout')
   
]
