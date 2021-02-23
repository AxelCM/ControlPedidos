#Django
from django.urls import path

#Views
from products.views import (list_product , create_product, MyProductsView,
    CreateProduct, UpdateProduct, DetailProduct , delete_product
    )

urlpatterns = [
    path('api/v1/list-product' , list_product, name='api_list_product' ),
    path('api/v1/create-product' , create_product, name='api_create_product'),
    path('mis-productos/' , MyProductsView.as_view(), name='my_products'),
    path('publish/product' , CreateProduct.as_view(), name='publish_product'),
    path('update/product/<int:pk>' , UpdateProduct.as_view(), name='update_product'),
    path('producto/<int:pk>' , DetailProduct.as_view(), name='detail_product'),
    path('eliminar-producto/' , delete_product, name='delete_product'),
]
