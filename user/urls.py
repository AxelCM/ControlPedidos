#Django
from django.urls import path

#Views
from user.views import SignUp
from sales.views import MyPurchase , MySales

urlpatterns = [
    path('registrarse/' , SignUp.as_view() , name='signup'),
    path('mis-compras/' , MyPurchase.as_view() , name='my_purchases'),
    path('mis-ventas/' , MySales.as_view() , name='my_sales'),
]
