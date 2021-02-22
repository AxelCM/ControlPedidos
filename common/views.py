#Django
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

#Django messages lib
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Django Permissions Mixins
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required ,permission_required
from django.utils.decorators import method_decorator

#Models
from products.models import Product


class NotPermissionsRule(LoginRequiredMixin,PermissionRequiredMixin):
    """Class for validate if a user have permission to render a view"""
    login_url = '/login/'
    raise_exception=False
    redirect_field_name="redirect_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='not_permission'
        return HttpResponseRedirect(reverse_lazy('not_permission'))

class NotPermissions(TemplateView):
    """View to redirect user a error for not permission to render"""
    template_name = 'common/error_404.html'

class CatalogueView(TemplateView):
    template_name = "common/customers/catalog.html"

    def get_context_data(self, *args , **kwargs):
        products = Product.objects.all()
        return {'data':products}

class LoginView(SuccessMessageMixin , auth_views.LoginView):
    template_name = 'common/login.html'
    success_message = "Bienvenido!"


class LogoutView(LoginRequiredMixin,SuccessMessageMixin, auth_views.LogoutView):
    success_message = "Cierre de sesion completado"
