#Django
from django.urls import path

#Views
from user.views import SignUp

urlpatterns = [
    path('registrarse/' , SignUp.as_view() , name='signup'),
]
