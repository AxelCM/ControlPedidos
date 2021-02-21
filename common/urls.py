#Django
from django.urls import path

#Views
from common.views import (CatalogueView, LoginView)

urlpatterns = [
    path('catalgo' , CatalogueView.as_view() , name='catalogue' ),
    path('login/' , LoginView.as_view() , name='login' )
]
