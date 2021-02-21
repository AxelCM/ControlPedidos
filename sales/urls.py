#Django
from django.urls import path

#Views
from sales.views import IndexView, CustomerView

urlpatterns= [
    path('', CustomerView.as_view(), name='index'),
    path('mydashboard/', IndexView.as_view(), name='customer_index'),
]
