from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from rest_framework.validators import UniqueTogetherValidator,UniqueValidator

class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = serializers.StringRelatedField()
    title = serializers.CharField(max_length= 255,
                                  validators=[ UniqueValidator(queryset=MenuItem.objects.all()),
                                              ])
    
    
    def validate(self, attrs):
        if attrs['price'] < 2:
            raise serializers.ValidationError("Invalid price: it must be greater than 2.")
        if attrs['inventory'] < 0:
            raise serializers.ValidationError("Invalid Stock: it must be a positive value.")
    
        return attrs

    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory','price_after_tax','category']
        


    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.025)

        