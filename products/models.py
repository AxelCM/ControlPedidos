#Django
from django.db import models
from django.conf import settings

#django-crum
from crum import get_current_user

#python
from datetime import datetime

#control the date of creation and modification of records and related users
class DataControl(models.Model):
    user_creation = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_creation'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_updated'
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    class Meta:
        abstract =  True

class Product(DataControl):
    """Model for products"""
    name = models.CharField('Name Product', max_length=100)
    cost_price = models.DecimalField('Cost price' , max_digits=10 , decimal_places=3)
    public_price = models.DecimalField('Public Price' ,max_digits=15, decimal_places=2)
    # slug = models.SlugField(null=True, blank=True)
    picture = models.ImageField(
        upload_to='products/pictures',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Product, self).save(*args, **kwargs)
