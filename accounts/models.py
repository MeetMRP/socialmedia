from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True)
    bio = models.TextField(blank=True)

    admin_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username + ' (' + self.designation() + ')'
    
    def designation(self):
        if self.is_superuser == True:
            return 'superuser'
        if self.is_staff == True:
            return 'staff'
        else:
            return 'user'