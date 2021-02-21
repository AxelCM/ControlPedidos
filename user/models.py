#Django
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    is_seller = models.BooleanField('Seller' , default=False)
    phone_number = models.CharField('Phone Number' , unique=True, max_length=12)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
