#Django
from django.db import models

#Models
from user.models import User
from products.models import DataControl, Product

#django-crum
from crum import get_current_user

#python
from datetime import datetime


class Sale(DataControl):
    address_ship = models.CharField('Direccion de envio', max_length=500, blank=True, null=True)
    total = models.DecimalField('Total Neto', decimal_places=2, max_digits=19, blank=True, null=True)

    def __str__(self):
        return self.address_ship

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Sale, self).save()

class DetailSale(DataControl):
    sale = models.ForeignKey(Sale, models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField('Cantidad')

    def __str__(self):
        return "{} - {}".format(self.product,self.cantidad)

    def save(self,*args,**kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(DetailSale, self).save(*args, **kwargs)
