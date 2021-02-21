from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy

#Djagno Permissions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from common.views import NotPermissionsRule

#Django Hasher passwords
from django.contrib.auth.hashers import make_password


#Models
from user.models import User

#forms
from user.forms import SignUpForm

class SignUp(SuccessMessageMixin,FormView):
    """Sign up to plattaform"""
    template_name = 'user/signup.html'
    form_class = SignUpForm
    success_message = "Gracias por registrarte a tienda Cian Coders empieza a comprar y a vender tus productos"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     now = datetime.now()
    #     self.object.date_joined = now
    #     password_plain = self.object.password
    #     password_hash = make_password(password_plain)
    #     self.object.password = password_hash
    #     self.object.save()
    #     return super(SignUp ,self).form_valid(form)
