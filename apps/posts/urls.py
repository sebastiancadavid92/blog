from rest_framework.routers import DefaultRouter

from apps.posts.views import PostCreateAPIView, PostGetDeleteAPIView

from django.urls import path

urlpatterns = [
    path('',PostCreateAPIView.as_view(),name='postcreation'),
    path('/<int:id>',PostGetDeleteAPIView.as_view(),name='getdeletepost')
]

