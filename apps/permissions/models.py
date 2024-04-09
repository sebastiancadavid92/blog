from django.db import models
from apps.posts.models import Post
# Create your models here.
class Category (models.Model):
    categoryname=models.CharField(unique=True,blank=True, null=True)

    def __str__(self):
        return self.category_name


class Permission (models.Model):
    permissionname=models.CharField(unique=True,blank=True)
    def __str__(self):
        return self.permission_name

class PermissionCategoryPost(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    permission=models.ForeignKey(Permission, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete= models.CASCADE)
    class Meta:
        constraints=[

            models.UniqueConstraint(fields=['post','category'], name='unique_post_n_category')
        ]
    def __str__(self):
        return str(self.post.id)+"->" +self.category.category_name +"="+ self.permission.permission_name
