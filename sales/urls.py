#Django
from django.urls import path

#Views
from sales.views import IndexView
urlpatterns= [
    path('', IndexView.as_view(), name='index')
]
