from django.db import models
from apps.posts.models import Post
# Create your models here.


CATEGORY_NAME_CHOICES=(
    ("PUBLIC","Public"),
    ("AUTHENTICATED","Authenticated"),
    ("TEAM","Team"),
    ("AUTHOR","Author")
    )
PERMISSION_NAME_CHOICES= (
    ("READ_ONLY","Read Only"),
    ("EDIT","Read and Edit"),
    ("NONE","None"),
    )


class Category (models.Model):
    categoryname=models.CharField( choices=CATEGORY_NAME_CHOICES,default=None)

    def __str__(self):
        return self.categoryname


class Permission (models.Model):
    permissionname=models.CharField(choices=PERMISSION_NAME_CHOICES,default=None)
    def __str__(self):
        return self.permissionname

class PermissionCategoryPost(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    permission=models.ForeignKey(Permission, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete= models.CASCADE,related_name='postinverse')
    class Meta:
        constraints=[

            models.UniqueConstraint(fields=['post','category'], name='unique_post_n_category')
        ]
    def __str__(self):
        return str(self.post.id)+"->" +self.category.category_name +"="+ self.permission.permission_name
