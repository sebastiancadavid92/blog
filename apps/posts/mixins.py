from django.db.models import Q
from rest_framework import mixins
from apps.posts.models import Post


class QuerysetMixin(mixins.ListModelMixin):

    def get_queryset(self):
    
        if not self.request.user.is_authenticated:
            return self.get_queryset_for_public()
        elif self.request.user.is_admin:
            return Post.objects.all()
        else:
            return self.get_queryset_for_authenticated_users()


    def get_queryset_for_authenticated_users(self):
        user=self.request.user
        query_part_1 = Q(author=user, postinverse__category__categoryname='AUTHOR',postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY'])
        query_part_2 = Q(author__team=user.team, postinverse__category__categoryname='TEAM', postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY']) & ~Q(author=user)
        query_part_3 = ~Q(author__team=user.team)&Q(postinverse__category__categoryname='AUTHENTICATED', postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY'])
        query = query_part_1 | query_part_2 | query_part_3
        queryset = Post.objects.filter(query).distinct().prefetch_related('postinverse__category','postinverse__permission')
        return queryset
    
    def get_queryset_for_public(self):
        query= Q(postinverse__category__categoryname='PUBLIC',postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY'])
        queryset = Post.objects.filter(query).distinct().prefetch_related('postinverse__category','postinverse__permission')
        return queryset