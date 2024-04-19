from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Post(models.Model):
    author=models.ForeignKey(User, on_delete= models.CASCADE)
    title= models.CharField(_('title'), max_length=255)
    content= models.TextField(_('content'), null=True, blank=True)
    timestamp= models.DateField(_('creation date'),auto_now_add=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_users_posts' ,blank=True)
    comments= models.ManyToManyField(User, through='Comment',related_name='comments_users_posts' ,blank=True)

    def like_exists(self,userid):
        return self.likes.filter(id=userid).exists()# se usa asi pur que likes ya es un objeto manager de usario 
    
    @property
    def exceptp(self):
        return self.content[:200]
    
    def __str__(self):
        return self.title
    


    
class Like (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(_('creation date'),auto_now_add=True)

    class Meta:
        constraints=[

            models.UniqueConstraint(fields=['user','post'], name='unique_user_n_post')
        ]

    def __str__(self):
        return self.user.username +" Likes "+ self.post.title
    

    
class Comment (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    content=models.TextField(_('content'))
    timestamp= models.DateField(_('creation date'),auto_now_add=True)

    def __str__(self):
        return self.user.username +" Comented On "+ self.post.title
    
