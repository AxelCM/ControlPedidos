#Django
from django.shortcuts import render
from django.views.generic import TemplateView

#REST Framework
from rest_framework.decorators import  api_view
from rest_framework.response import Response

#Models
from products.models import Product

#Serialiezers
from products.serializers import ProductSerializer


class IndexView(TemplateView):
    template_name = "common/index.html"


class CustomerView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        # my_products = Product.objects.filter(user_creation=me)
        my_products = Product.objects.all()
        return {"data": my_products}

class MyProductsView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, *args , **kwargs):
        me = self.request.user.pk
        my_products = Product.objects.filter(user_creation=me)
        return {"data": my_products}




@api_view(['GET'])
def list_product(request):
    products = Product.objects.all()
    for p in products:
        serializer = ProductSerializer(p)
        data.append(serializer.data)
    return Response(data)
# class MyInventory(TemplateView):
#     template_name = "common"
