from rest_framework.routers import DefaultRouter

from apps.posts.views import PostCreateListAPIView, PostGetDeleteUpdateAPIView,LikeAPIView,CommentAPIView

from django.urls import path

urlpatterns = [
    path('',PostCreateListAPIView.as_view(),name='postcreationlist'),
    path('<pk>/',PostGetDeleteUpdateAPIView.as_view(),name='getdeletepost'),
    path('<pk>/like/',LikeAPIView.as_view(),name='likeapost'),
    path('<pk>/like/<pkc>/',LikeAPIView.as_view(),name='likeapost'),
    path('<pk>/comment/<pkc>/',CommentAPIView.as_view(),name='deletecomment'),
    path('<pk>/comment/',CommentAPIView.as_view(),name='commentapost')
]


