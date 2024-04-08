from django.db import models
from apps.posts.models import Post
# Create your models here.
class Category (models.Model):
    category_name=models.CharField(unique=True,blank=True, null=True)

    def __str__(self):
        return self.category_name


class Permission (models.Model):
    permission_name=models.CharField(unique=True,blank=True)
    def __str__(self):
        return self.permission_name

class Permission_Category_Post(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    permission=models.ForeignKey(Permission, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete= models.CASCADE)
    class Meta:
        constraints=[

            models.UniqueConstraint(fields=['post','category'], name='unique_post_n_category')
        ]
    def __str__(self):
        return str(self.post.id)+"->" +self.category.category_name +"="+ self.permission.permission_name
