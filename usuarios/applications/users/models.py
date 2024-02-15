from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    
    GENERO_CHOICES = (
        ('F','Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otro'),
    )
    
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100)
    nombres = models.CharField(max_length=50, blank= True)
    apellidos = models.CharField(max_length=50, blank= True)
    genero = models.CharField(max_length=1, choices = GENERO_CHOICES, blank= True)
    
    codregistro = models.CharField(max_length=6, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = ['email',]
    
    objects = UserManager()
    
    
    def get_short_name(self):
        return self.username
    
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos