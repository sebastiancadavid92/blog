from rest_framework.routers import DefaultRouter

from apps.users.views import login_view



from django.urls import path

urlpatterns = [
    path('login/',login_view,name='loginv'),
   
]
