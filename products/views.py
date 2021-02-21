#Django
from django.shortcuts import render

#REST Framework
from rest_framework.decorators import  api_view
from rest_framework.response import Response

#Models
from products.models import Product

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
