
from rest_framework.generics import GenericAPIView,ListCreateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from django.db.models import Q

from apps.posts.serializer import CreationPostModelSerializer,LikeModelSerializer
from .models import Post,Like,Comment
from .permissionclass import PostPermissionRead, PostPermissionEdit
from .pagiantionclasses import Pagination
# Create your views here.

class PostCreateListAPIView(ListCreateAPIView):

    serializer_class=CreationPostModelSerializer
    pagination_class=Pagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return [AllowAny()]
       

    def get_queryset1(self):
        user=self.request.user
        query_part_1 = Q(author=user, postinverse__category__categoryname='AUTHOR',postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY'])
        query_part_2 = Q(author__team=user.team, postinverse__category__categoryname='TEAM', postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY']) & ~Q(author=user)
        query_part_3 = ~Q(author__team=user.team)&Q(postinverse__category__categoryname='AUTHENTICATED', postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY'])
        query = query_part_1 | query_part_2 | query_part_3
        queryset = Post.objects.filter(query).distinct().prefetch_related('postinverse__category','postinverse__permission')
        return queryset
    
    def get_queryset2(self):
        query= Q(postinverse__category__categoryname='PUBLIC',postinverse__permission__permissionname__in=['EDIT', 'READ_ONLY'])
        queryset = Post.objects.filter(query).distinct().prefetch_related('postinverse__category','postinverse__permission')
        return queryset


    def list(self, request, *args, **kwargs):
        #import pdb;pdb.set_trace()

        if not self.request.user.is_authenticated:
           query=self.get_queryset2()
           if len(query)==0:
                return Response({},status=status.HTTP_200_OK)
           
           page = self.paginate_queryset(query.order_by('id'))

           if page is not None:
              serializer = self.get_serializer(page, many=True)
              return Response( self.get_paginated_response(serializer.data),status=status.HTTP_200_OK)
           # Devuelve la respuesta sin paginación
            
        elif self.request.user.is_admin:
            query=Post.objects.all()
            if len(query)==0:
                return Response({},status=status.HTTP_200_OK)
            #####
            page = self.paginate_queryset(query.order_by('id'))
            if page is not None:
              serializer = self.get_serializer(page, many=True)
              return Response( self.get_paginated_response(serializer.data),status=status.HTTP_200_OK)
           
        
        else:
            query=self.get_queryset1()
            if len(query)==0:
                return Response({},status=status.HTTP_200_OK)
            page = self.paginate_queryset(query.order_by('id'))
            if page is not None:
              serializer = self.get_serializer(page, many=True)
              return Response( self.get_paginated_response(serializer.data),status=status.HTTP_200_OK)




    def post(self,request):
        author=request.user
        serializerblog=self.serializer_class(data=request.data, context={'author':author})
        if serializerblog.is_valid():
            blog=serializerblog.save()
            data=self.serializer_class(blog)
            if len(serializerblog.errors)==0:
                return Response(data.data,status=status.HTTP_201_CREATED) 
        return Response(serializerblog.errors,status=status.HTTP_400_BAD_REQUEST)


class PostGetDeleteUpdateAPIView(RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,GenericAPIView): 
    serializer_class=CreationPostModelSerializer
    queryset=Post.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [PostPermissionRead()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [PostPermissionEdit()]
      

     
    def patch(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
 
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
 
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class LikeAPIView(GenericAPIView):
    queryset=Post.objects.all()
    permission_classes=[PostPermissionRead,IsAuthenticated]
    
    def post(self, request, pk):      
        post=self.get_object()
        if post.like_exists(request.user.id):
            return Response({'error':'This user already liked this post'},status.HTTP_400_BAD_REQUEST)
        like=Like.objects.create(user=request.user, post=post)
        serializer=LikeModelSerializer(like)
        return Response(serializer.data,status.HTTP_201_CREATED)
    
    def delete(self,request,pk):
        post=post=self.get_object()
        if post.like_exists(request.user.id):
            like=Like.objects.filter(post=post,user=request.user)
            like.delete()
            return Response({"messange":"sucessful like delete"},status.HTTP_204_NO_CONTENT)
        return Response({'error':'no like found'},status.HTTP_400_BAD_REQUEST)
        