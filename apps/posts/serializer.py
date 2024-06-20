from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.posts.models import Post,Like,Comment
from apps.permissions.models import Category,Permission, PermissionCategoryPost
from apps.permissions.models import CATEGORY_NAME_CHOICES,PERMISSION_NAME_CHOICES
from django.db import transaction


class PermissionCategoryPostModelSerializer(ModelSerializer):
    class Meta:
        model=PermissionCategoryPost
        fields=['post','category','permission']


class CreationPostModelSerializer(ModelSerializer):
    permissions=serializers.ListField(write_only=True)
    categories=serializers.ListField(write_only=True)
    class Meta:
        model=Post
        fields=['title','content','permissions','id','categories']


    def to_internal_value(self, data):
        if  'permission' in data and data['permission']:
            per=data.pop('permission')
            data['permissions']=[{'permissionname':i }for i in per.values()]
            data['categories']=[{'categoryname':i }for i in per.keys()]
            return super().to_internal_value(data)
        raise serializers.ValidationError({'error':'the field permission has to be provided and not empty for post creation'})
    
    

    def validate_permissions(self,value):
        lista=[i[0]for i in PERMISSION_NAME_CHOICES]
        per=[i['permissionname'] for i in value]
        if len(per)!= len(CATEGORY_NAME_CHOICES):
            raise serializers.ValidationError({'error':'some permissions are missed'})
        if any(i not in lista for i in per):
            raise serializers.ValidationError({'error':'permissions name are not defined correctly'})
        seri=PermissionModelSerializer(data=value,many=True)
        if not seri.is_valid():
            raise serializers.ValidationError(seri.errors)
        self.context['permissionserializer']=seri
        return value


    def validate_categories(self,value):
        lista=[i[0] for i in CATEGORY_NAME_CHOICES]
        tuplas = [tuple(sorted(d.items())) for d in value]
        if len(tuplas)!=len(set(tuplas)):
            raise serializers.ValidationError({"error":"categories where not defined correctly"})  
        if len(CATEGORY_NAME_CHOICES)!=len(set(tuplas)):
            raise serializers.ValidationError({'Category name':'your post hasnt defined the Category permission correctly'})
        if any (tuplas[i][0][1] not in lista for i in range(0,len(value))):
            raise serializers.ValidationError({'Category name':'your post hasnt defined the Category permission correctly'})
        
        seri=CategoryModelSerializer(data=value,many=True)
        if not seri.is_valid():
            raise serializers.ValidationError(seri.errors)
        self.context['categoryserializer']=seri
        return value

    def validate(self, attrs):
        
        attrs.pop('permissions')
        attrs.pop('categories')
        return attrs


    @transaction.atomic
    def create(self, validated_data):

        catserializer=self.context['categoryserializer']
        perserializer=self.context['permissionserializer']
        try :
            categories=catserializer.save()
            permissions=perserializer.save()
            author=self.context['author']
            blog=Post.objects.create(author=author,**validated_data)
            data = [{'post':blog.id, 'category':categories[i][0].id,'permission':permissions[i][0].id} for i in range(0,len(categories))] 
           
            categorypermissionpost=PermissionCategoryPostModelSerializer(data=data,many=True)
            
            if not categorypermissionpost.is_valid():
                raise serializers.ValidationError({'error'})
            if len(self.errors)!=0:
                raise serializers.ValidationError({'error'})
            
            cpp=categorypermissionpost.save()
            self.context['postcategorypermission']=cpp 
            return blog

        except Exception:
            raise serializers.ValidationError({'error':'an error has ocurred while trying to save category permission and post on the database'})
        
       
    
    def to_representation(self,instance):
            rep=dict()
            rep['id']=instance.id
            rep['author_name']=instance.author.username
            rep['author_id']=instance.author.id
            rep['title']=instance.title
            rep['excerpt']=instance.exceptp
            rep['team_name']=instance.author.team.team_name
            rep['team_id']=instance.author.team.id
            rep['timestamp']=(instance.timestamp)
            rep['comments']=instance.comments.all().count()
            rep['likes']=instance.likes.all().count()
            rep['content']=instance.content
            per=instance.postinverse.all()
            rep['permission']={i.category.categoryname : i.permission.permissionname for i in per} 
            rep['edit']=self.__can_edit(self.context.get('request').user,instance,rep['permission'])
            rep['liked']=instance.like_exists(self.context.get('request').user.id)
            return rep
    
                
    def __can_edit(self,user,post:Post, permissiondict):
        team=post.author.team
        if (not user.is_authenticated) and (permissiondict.get('PUBLIC')=='NONE' or permissiondict.get('PUBLIC')=='READ_ONLY'):
            return False
        elif (not user.is_authenticated) and (permissiondict.get('PUBLIC')=='EDIT'):
            return True     
        if user.is_admin:
            return True
        if user==post.author and (permissiondict.get('AUTHOR')=='NONE' or permissiondict.get('AUTHOR')=='READ_ONLY'):
            return False
        elif user==post.author and (permissiondict.get('AUTHOR')=='EDIT'):
            return True
        if team==user.team and (permissiondict.get('TEAM')=='NONE' or permissiondict.get('TEAM')=='READ_ONLY'):
            return False
        elif user.team==team and (permissiondict.get('TEAM')=='EDIT' ):
            return True
        if user.is_authenticated and (permissiondict.get('AUTHENTICATED')=='NONE' or permissiondict.get('AUTHENTICATED')=='READ_ONLY'):
            return False
        elif user.is_authenticated and (permissiondict.get('AUTHENTICATED')=='EDIT'):
            return True
    
    
    @transaction.atomic
    def update(self, instance, validated_data):        
        instance.title=validated_data.get('title')
        instance.content=validated_data.get('content')
        cate=self.context['categoryserializer'].save()
        perm=self.context['permissionserializer'].save()
        instance.postinverse.all().delete()
        for i in range(0,len(cate)):
            PermissionCategoryPost.objects.create(post=instance,category=cate[i][0],permission=perm[i][0])
        instance.save()
        return instance

class CategoryModelSerializer(ModelSerializer):

    class Meta:
        model=Category
        fields = ['categoryname']
    
    def create(self,validated_data):
        category=Category.objects.get_or_create(**validated_data)
        return category

class PermissionModelSerializer(ModelSerializer):
    class Meta:
        model=Permission
        fields = '__all__'
    
    def create(self,validated_data):
        permission=Permission.objects.get_or_create(**validated_data)
        return permission


class LikeModelSerializer(ModelSerializer):
    class Meta:
        model=Like
        fields = '__all__'
        
    def to_representation(self,instance):
        rep={
                'username':instance.user.username,
                'post':instance.post.title,
                'timestamp':instance.timestamp.strftime('%Y-%m-%d %H:%M')
                
                
            }
        return rep
    
class CommentModelSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields = '__all__'
    

    def validate(self,validated_data):
        if not 'content' in validated_data:
            raise serializers.ValidationError({"error content":"content has to be prived"})
        if not validated_data.get('content'):
            raise serializers.ValidationError({"error content":"content cant be null"})
        return validated_data 
    
    def to_internal_value(self, data):
        data['user']=self.context.get('user')
        data['post']=self.context.get('post')
        return data

    def create(self, validated_data):
   
        comment=Comment.objects.create(**validated_data)
        
        return comment

    def to_representation(self,instance):
        rep={   
                'id':instance.id,
                'username':instance.user.username,
                'post':instance.post.title,
                'content':instance.content,
                'timestamp':instance.timestamp.strftime('%Y-%m-%d %H:%M')
                
                
            }
        return rep
    