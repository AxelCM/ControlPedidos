#Django
from django import forms

#django-crum
from crum import get_current_user

#Models
from products.models import Product

class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
        'name',
        'cost_price',
        'public_price',
        'user_creation',
        'picture'
        )


# class CreateProductForm(forms.Form):
#     """Create Product Form"""
#     cost_price = forms.CharField(
#         max_length=50,
#         widget=forms.DecimalField()
#     )
#     public_price = forms.CharField(
#         max_length=50,
#         widget=forms.DecimalField()
#     )
#     name = forms.CharField(
#         min_length=5,
#         max_length=50
#     )
