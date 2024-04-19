from apps.posts.views import ListCommentsAPIView
from django.urls import path

urlpatterns = [path('',ListCommentsAPIView.as_view(),name='listcoments')]