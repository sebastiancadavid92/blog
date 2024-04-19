from rest_framework.routers import DefaultRouter

from apps.posts.views import PostCreateListAPIView, PostGetDeleteUpdateAPIView,LikeAPIView

from django.urls import path

urlpatterns = [
    path('',PostCreateListAPIView.as_view(),name='postcreationlist'),
    path('<pk>/',PostGetDeleteUpdateAPIView.as_view(),name='getdeletepost'),
    path('<pk>/like/',LikeAPIView.as_view(),name='likeapost')
]

