#Django
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q , Count, Avg, Sum
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
from sales.models import Sale,DetailSale

#Forms
from sales.forms import SaleForm, DetailSaleForm

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
        my_products = Product.objects.filter(~Q(user_creation=me))
        init_cart = initCart(self.request)
        if init_cart:
            cart_counter = len(init_cart)
        else:
            cart_counter = 0
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
    return HttpResponseRedirect(reverse_lazy('index'))

def list_items(cart):
    """ parser ids in the card to filter in CartView"""
    item_id_list = []
    if cart:
        for c in cart:
            if Product.objects.filter(pk=c['pk']).exists():
                item_id_list.append(c['pk'])
    return item_id_list

def calc_total(cart):
    """Calculate all items in cart"""
    total = 0
    if cart:
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
        if init_cart:
            list = list_items(init_cart)
        else:
            list = []
        total = calc_total(init_cart)
        if init_cart:
            cart_counter = len(init_cart)
        else:
            cart_counter = 0
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

def related_items(request, sale):
    cart = request.session["cart"]
    sale = sale
    if cart:
        for c in cart:
            if Product.objects.filter(pk=c['pk']).exists():
                product = Product.objects.get(pk=c['pk'])
                detail = DetailSale.objects.create(
                product=product,
                sale=sale,
                cantidad =c['cant'],
                )
                detail.save()

class CreateSale(SuccessMessageMixin, LoginRequiredMixin,CreateView):
    # permission_required = "products.add_product"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'sales/modals/checkout.html'
    form_class = SaleForm
    success_message = 'Felicidades tu compra se ha procesado con exito'
    success_url = reverse_lazy('clean_cart')


    """Validate and relate data for sale"""
    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user.pk
        me = User.objects.get(pk=user)
        cart = self.request.session["cart"]
        self.object.total = calc_total(cart)
        self.object.save()
        id=self.object.id
        sale = Sale.objects.get(pk=id)
        related_items(self.request, sale)
        return super(CreateSale, self).form_valid(form)

class MyPurchase(TemplateView):
    template_name = "user/my_purchase.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        my_purchases= Sale.objects.filter(user_creation__pk=me)
        detail_items = DetailSale.objects.filter(user_creation__pk=me)
        return {"data": my_purchases , 'detail_items':detail_items}

def calculate_profits(request):
    pass

class MySales(TemplateView):
    template_name = "user/my_sales.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        sales_items = []
        global_counter = {}
        global_times = 0
        total_profit = []
        my_sales= Sale.objects.all()
        products = DetailSale.objects.filter(product__user_creation__pk=me).order_by('product__pk')
        count = products.annotate(cantidad_sold=Sum('cantidad'))
        profit = products.aggregate(total_profit=Sum('sale__total'))
        profit_parsed = 'Q{:,.2f}'.format(profit['total_profit'])
        for p in products:
            counter = DetailSale.objects.filter(product__pk=p.product.pk)
            sold = counter.aggregate(cantidad_sold=Sum('cantidad'))
            price = counter.aggregate(price_avg=Avg('product__public_price'))
            profit = (price['price_avg'] - p.product.cost_price) * sold['cantidad_sold']
            global_counter.update({p.product.name:"{} Unidad(es) / Q{:.2f} ----Q{:.2f} de ganancia total".format(sold['cantidad_sold'] , price['price_avg'], profit)})
        dict_no_duplicados = {}
        for key, value in global_counter.items():
            if not value in dict_no_duplicados.values():
                dict_no_duplicados[key] = value
        return {"data": dict_no_duplicados , "total_profit": profit_parsed}
