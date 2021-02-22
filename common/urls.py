#Django
from django.urls import path

#Views
from common.views import (CatalogueView, LoginView, LogoutView, NotPermissions

    )

urlpatterns = [
    path('catalgo' , CatalogueView.as_view() , name='catalogue' ),
    path('login/' , LoginView.as_view() , name='login'),
    path('logout/' , LogoutView.as_view() , name='logout'),
    path('error/', NotPermissions.as_view(), name='not_permission'),

]
