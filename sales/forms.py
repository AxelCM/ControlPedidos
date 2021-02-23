#Django
from django import forms

#django-crum
from crum import get_current_user

#Models
from sales.models import Sale,DetailSale

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = (
        'address_ship',
        )

class DetailSaleForm(forms.ModelForm):

    class Meta:
        model = DetailSale
        fields = (
        'sale',
        'product',
        'cantidad'
        )
