from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.posts.models import Post
from apps.permissions.models import Category,Permission, PermissionCategoryPost
from apps.permissions.models import CATEGORY_NAME_CHOICES,PERMISSION_NAME_CHOICES



class PermissionCategoryPostModelSerializer(ModelSerializer):
    class Meta:
        model=PermissionCategoryPost
        fields=['post','category','permission']


class CreationPostModelSerializer(ModelSerializer):
    permission=serializers.DictField(write_only=True)
    class Meta:
        model=Post
        fields=['title','content','permission','id']

    def validate_permission(self,value):
        #import pdb;pdb.set_trace()
            
        if len(CATEGORY_NAME_CHOICES)!=len(set(value)):
            raise serializers.ValidationError({'Category name':'your post hasnt defined the Category permission correctly'})
        if len(CATEGORY_NAME_CHOICES)!=len(value):
             raise serializers.ValidationError({'Category name':'your post hasnt defined the Category permission correctly'})
        
        return value

    def save(self, **kwargs):
        
        permission=self.validated_data.pop('permission')
        import pdb;pdb.set_trace()
        blog=super().save(**kwargs)
        return blog,permission

    def  to_representation(self,instance):
        representation=super(). to_representation(instance)
        #import pdb;pdb.set_trace()
        representation['permission']={i.category.categoryname:i.permission.permissionname for i in instance.postinverse.all()}
        return representation




class CategoryModelSerializer(ModelSerializer):

    class Meta:
        model=Category
        fields = ['categoryname']
    

    """ def validate_categoryname(self, value):
        if  not any(value==choice[0] for choice in CATEGORY_NAME_CHOICES):
            raise serializers.ValidationError({'error':f"the category {value} is not allowed "})
        return value """
    
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
    
"""     def validate_permissionname(self, value):
        if not any(value==choice[0] for choice in PERMISSION_NAME_CHOICES):
            raise serializers.ValidationError({'error':f"the permission {value} is not allowed "})
        return value """
    
