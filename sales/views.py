#Django
from django.shortcuts import render
from django.views.generic import TemplateView

#REST Framework
from rest_framework.decorators import  api_view
from rest_framework.response import Response

#Models
from products.serializers import ProductSerializer

# Create your views here.
class IndexView(TemplateView):
    template_name = "common/index.html"


class CustomerView(TemplateView):
    template_name = "common/index.html"




@api_view(['GET'])
def list_product(request):
    products = Product.objects.all()
    for p in products:
        serializer = ProductSerializer(p)
        data.append(serializer.data)
    return Response(data)
# class MyInventory(TemplateView):
#     template_name = "common"
