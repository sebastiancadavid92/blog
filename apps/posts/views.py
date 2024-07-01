
from rest_framework.generics import GenericAPIView,ListCreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin



from apps.posts.serializer import CreationPostModelSerializer,LikeModelSerializer,CommentModelSerializer
from .models import Post,Like,Comment
from .permissionclass import PostPermissionRead, PostPermissionEdit
from .pagiantionclasses import Pagination,PaginationLike,PaginationComments
from .mixins import QuerysetMixin
from .filter import LikeFilter,CommentFilter
# Create your views here.

class PostCreateListAPIView(QuerysetMixin,ListCreateAPIView):

    serializer_class=CreationPostModelSerializer
    pagination_class=Pagination
  

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return [AllowAny()]

    def list(self, request, *args, **kwargs):
        query=self.get_queryset()
        if len(query)==0:
                return Response({},status=status.HTTP_200_OK)
           
        page = self.paginate_queryset(query)
        if page is not None:
              serializer = self.get_serializer(page, many=True)
              return Response( self.get_paginated_response(serializer.data),status=status.HTTP_200_OK)
           # Devuelve la respuesta sin paginación


    def post(self,request):
      
        author=request.user
        serializerblog=self.serializer_class(data=request.data, context={'author':author})
        if serializerblog.is_valid():
            blog=serializerblog.save()
            data=self.serializer_class(blog,context={'request':request})
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
            return Response({'error':'This user already liked this post'},status.HTTP_403_FORBIDDEN)
        like=Like.objects.create(user=request.user, post=post)
        serializer=LikeModelSerializer(like)
        return Response(serializer.data,status.HTTP_201_CREATED)
    
    def delete(self,request,pk,pkc=None):
        post=post=self.get_object()
        if post.like_exists(request.user.id):
            like=Like.objects.filter(post=post,user=request.user)
            like.delete()
            return Response({"messange":"sucessful like delete"},status.HTTP_204_NO_CONTENT)
        return Response({'error':'no like found'},status.HTTP_404_NOT_FOUND)
    

class CommentAPIView(GenericAPIView):
    queryset=Post.objects.all()
    permission_classes=[PostPermissionRead,IsAuthenticated]
    lookup_url_kwarg = 'pk'
    

    def post(self, request, pk):      
        post=self.get_object()
        serializer=CommentModelSerializer(data=request.data,context={"request":request,"user":request.user,"post":post})
        if not serializer.is_valid():
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status.HTTP_201_CREATED)
    
    def delete(self,request,pk,pkc=None):
        
        post=self.get_object()
        comment=Comment.objects.prefetch_related('user').filter(id=pkc).first()
        if comment and comment.user==request.user:
            comment.delete()
            return Response({"messange":"sucessful comment delete"},status.HTTP_204_NO_CONTENT)
        if not comment:
            return Response({'error':'comment not found'},status.HTTP_404_NOT_FOUND)
        if comment.user!=request.user:
            return Response({'error':'not allowed to delete this cooment'},status.HTTP_403_FORBIDDEN)


class ListLikeAPIView(QuerysetMixin,ListAPIView):
    serializer_class=LikeModelSerializer
    pagination_class=PaginationLike

    def get_queryset(self):
        query=Like.objects.filter(post__in=super().get_queryset()).prefetch_related('post','user')
        return LikeFilter(self.request.GET, query).qs

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        page = self.paginate_queryset(queryset.order_by('id'))
        serializer=LikeModelSerializer(page,many=True)
        return Response(self.get_paginated_response(serializer.data),status.HTTP_200_OK)
        

class ListCommentsAPIView(QuerysetMixin,ListAPIView):
    serializer_class=CommentModelSerializer
    pagination_class=PaginationComments


    def get_queryset(self):
        query=Comment.objects.filter(post__in=super().get_queryset()).prefetch_related('post','user').order_by('-timestamp')
        return CommentFilter(self.request.GET, query).qs
    
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        page = self.paginate_queryset(queryset.order_by('id'))
        serializer=self.get_serializer(page,many=True)
        return Response(self.get_paginated_response(serializer.data),status.HTTP_200_OK)
    
    