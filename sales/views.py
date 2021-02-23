#Django
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

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

#Serialiezers
from products.serializers import ProductSerializer

def initCart(request):
    """initial cart in the request sessions django"""
    if not 'cart' in request.session or not request.session['cart']:
        cart = request.session["cart"] = []
    else:
        """Update if remove some product"""
        cart = request.session["cart"]
        for i in range(len(cart)-1):
            if Product.objects.filter(pk=cart[i]['pk']).exists() == False:
                del cart[i]
        return cart

class IndexView(TemplateView):
    template_name = "common/index.html"


class CustomerView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        # my_products = Product.objects.filter(user_creation=me)
        my_products = Product.objects.all()
        init_cart = initCart(self.request)
        cart_counter = len(init_cart)
        return {"data": my_products , 'cart_counter':cart_counter}

class MyProductsView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        my_products = Product.objects.filter(user_creation=me)
        return {"data": my_products}


def add_to_cart(request):
    """Add item in the cart session, add cant and id for calculate after"""
    me = User.objects.get(pk=request.user.pk)
    id = request.POST.get('product' , '')
    cant = request.POST.get('cant' , '')
    cart = []
    data = Product.objects.get(pk=id)
    cart = request.session["cart"]
    if data.user_creation == me:
        messages.error(request, 'No puedes agregar tu propio producto al carrito'.format(data.name))
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        cart.append({'pk':data.pk, 'cant':cant})
        request.session["cart"] = cart
        messages.success(request, 'Se agrego {} a tu carrito'.format(data.name))
        return HttpResponseRedirect(reverse_lazy('index'))

def clean_cart(request):
    """clean cart in the request sessions django"""
    if  'cart' in request.session or request.session['cart']:
        cart = request.session["cart"] = []
    return HttpResponseRedirect(reverse_lazy('my_cart'))

def list_items(cart):
    """ parser ids in the card to filter in CartView"""
    item_id_list = []
    for c in cart:
        if Product.objects.filter(pk=c['pk']).exists():
            item_id_list.append(c['pk'])
    return item_id_list

def calc_total(cart):
    """Calculate all items in cart"""
    total = 0
    for c in cart:
        if Product.objects.filter(pk=c['pk']).exists():
            product = Product.objects.get(pk=c['pk'])
            cant = int(c['cant'])
            price = float(product.public_price)
            total += cant*price
    return float("{:.2f}".format(total))

def pop_cart(request):
    id = request.POST.get('product' , '')
    data = request.session["cart"]
    for i in range(len(data)):
        if data[i]['pk'] == int(id):
            del data[i]
            break
    request.session["cart"] = data
    messages.success(request, "Eliminaste el articulo de tu carrito")
    return HttpResponseRedirect(reverse_lazy('my_cart'))

class CartView(TemplateView):
    template_name = 'sales/cart.html'

    def get_context_data(self , *args , **kwargs):
        init_cart = initCart(self.request)
        list = list_items(init_cart)
        total = calc_total(init_cart)
        cart_counter = len(init_cart)
        cart = Product.objects.filter(pk__in=list)
        return {'cart_counter':cart_counter , 'cart':cart, 'init_cart':init_cart , 'total':total}


@api_view(['GET'])
def list_product(request):
    products = Product.objects.all()
    for p in products:
        serializer = ProductSerializer(p)
        data.append(serializer.data)
    return Response(data)
# class MyInventory(TemplateView):
#     template_name = "common"
