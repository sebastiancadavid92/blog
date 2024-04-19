import django_filters
from .models import Like
from .models import Comment


class LikeFilter(django_filters.FilterSet):

    post = django_filters.NumberFilter(field_name='post__id', lookup_expr='exact')
    user = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Like
        fields = ['post', 'user']

class CommentFilter(django_filters.FilterSet):
    
    post = django_filters.NumberFilter(field_name='post__id', lookup_expr='exact')
    user = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Comment
        fields = ['post', 'user']