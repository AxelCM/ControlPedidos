#Django
from django.urls import path

#Views
from sales.views import (IndexView, CustomerView , add_to_cart, CartView, clean_cart,
    pop_cart,
    )

urlpatterns= [
    path('', CustomerView.as_view(), name='index'),
    path('mydashboard/', IndexView.as_view(), name='customer_index'),
    path('agregar-al-carrito/', add_to_cart, name='add_to_cart'),
    path('vaciar-carrito-de-compra/', clean_cart, name='clean_cart'),
    path('borrar-de-carrito/', pop_cart, name='pop_cart'),
    path('mi-carrito/', CartView.as_view(), name='my_cart'),
]
