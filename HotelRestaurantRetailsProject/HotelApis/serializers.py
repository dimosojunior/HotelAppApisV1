from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 
        
class HotelInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInventory
        fields = '__all__' 

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__' 


class CartItemsSerializer(serializers.ModelSerializer):
	cart = CartSerializer()
	product = ProductSerializer()
	class Meta:
		model = CartItems
		fields = '__all__' 



