#Django
from django.urls import path

#Views
from products.views import list_product , create_product

urlpatterns = [
    path('api/v1/list-product' , list_product, name='api_list_product' ),
    path('api/v1/create-product' , create_product, name='api_create_product'),
]
