#Django
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView

#Django messages lib
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Django Permissions Mixins
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.contrib.auth import views as auth_views
from common.views import NotPermissionsRule


#REST Framework
from rest_framework.decorators import  api_view
from rest_framework.response import Response

#Models
from products.models import Product
from user.models import User

#Forms
from products.forms import CreateProductForm

#Serializers
from products.serializers import (
ProductSerializer, CreateProductSerializer,
)

@api_view(['GET'])
def list_product(request):
    data = []
    products = Product.objects.all()
    for p in products:
        serializer = ProductSerializer(p)
        data.append(serializer.data)
    return Response(data)

@api_view(['POST'])
def create_product(request):
    serializer = CreateProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save()
    return Response(CreateProductSerializer(product).data)

class MyProductsView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        my_products = Product.objects.filter(user_creation=me)
        is_owner = True
        create = True
        edit = True
        return {"data": my_products , 'is_owner':is_owner, 'create':create , 'edit':edit}

class CreateProduct(SuccessMessageMixin, LoginRequiredMixin,CreateView):
    # permission_required = "products.add_product"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'common/index.html'
    form_class = CreateProductForm
    success_message = 'Tu producto ha sido publicado'
    success_url = reverse_lazy('my_products')


class UpdateProduct(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    login_url= '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'common/index.html'
    model = Product
    fields = ['name' , 'cost_price' , 'public_price' , 'picture']
    success_message = 'El producto fue actualizado correctamente'
    success_url = reverse_lazy('my_products')

    def form_valid(self, form):
        me = User.objects.get(pk=self.request.user.pk)
        if self.object.user_creation == me:
                self.object.save()
                return super(UpdateProduct, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('not_permission'))

    def get_context_data(self , *args , **kwargs):
        context = super(UpdateProduct, self).get_context_data(**kwargs)
        id_product = self.get_object()
        context['edit'] = True
        return context


class DeleteProduct(DeleteView):
    pass

class DetailProduct(LoginRequiredMixin,DetailView):
    login_url= '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'products/detail_product.html'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self , *args , **kwargs):
        context = super(DetailProduct, self).get_context_data(**kwargs)
        id_product = self.get_object()
        return context
