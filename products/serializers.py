#Product serializer data

#Django
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from products.models import Product

class ProductSerializer(serializers.Serializer):
    #List products serializer
    id = serializers.IntegerField()
    name = serializers.CharField()
    cost_price = serializers.FloatField()
    public_price = serializers.FloatField()

class CreateProductSerializer(serializers.Serializer):
    #Create product serializer
    name = serializers.CharField(
        max_length=100,
        validators = [UniqueValidator(queryset=Product.objects.all())]
        )
    cost_price = serializers.FloatField(min_value=0)
    public_price = serializers.FloatField(min_value=0)

    def create(self, data):
        return Product.objects.create(**data)
