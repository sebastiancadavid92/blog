from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _



class Team(models.Model):
    
    team_name=models.CharField(_('team name'),max_length=255,unique=True)


    def __str__(self):
        return self.team_name



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create(self, **kwargs):
        
        return self.create_user(**kwargs)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin',True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    first_name=models.CharField(_('first name'),max_length= 255, blank=True, null=True) 
    last_name=models.CharField(_('last name'),max_length= 255, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    username=models.CharField(_('user name'),unique=True,blank=False, null=False)
    birthdate=models.DateField(_('birth date'), blank=True, null=True)
    team=models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin=models.BooleanField(_('admin'),default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 