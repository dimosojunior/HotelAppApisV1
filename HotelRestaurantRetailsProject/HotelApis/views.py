from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,get_object_or_404
from .serializers import *
from .models import *
from .serializers import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .serializers import *
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

# 	def get(self,request, format=None):
# 		return Response("User Account View", status=200)

# 	def post(self,request, format=None):

# 		return Response("Creating User", status=200)



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed










#-----------------------------------------------


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HotelApis.models import MyUser  # Make sure to import your MyUser model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def HotelView(request):

	return HttpResponse("Hotel")


@api_view(['GET'])
def HotelFoodProductsView(request):
	if request.method == "GET":
		products = Product.objects.all()
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def HotelInventoryFoodView(request):
	if request.method == "GET":
		products = HotelInventory.objects.all()
		serializer = HotelInventorySerializer(products, many=True)
		return Response(serializer.data)



class CartView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	# kama unatumia JWT weka hiyo tu
	# permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
	def get(self, request):
		user = request.user
		cart = Cart.objects.filter(user=user, ordered=False).first()
		queryset = CartItems.objects.filter(cart=cart)
		serializer = CartItemsSerializer(queryset, many=True)

		return Response(serializer.data)



#ADD ITEM TO A CART
#Eg:
# {
#     "product":1,
#     "quantity":5
# }
	def post(self, request):
		data = request.data
		user = request.user
		cart,_ = Cart.objects.get_or_create(user=user, ordered=False)
		product = Product.objects.get(id=data.get('product'))
		price = product.price
		quantity = data.get('quantity')
		cart_items = CartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
		cart_items.save()

		cart_items = CartItems.objects.filter(user=user, cart=cart.id)

		total_price=0
		for items in cart_items:
			total_price += items.price
		cart.total_price = total_price
		cart.save()
		return Response({'success': 'Items Added To Your Cart'})


#TO UPDATE CART ITEMS
#Eg:
# {
#     "id":11,
#     "quantity":6   
# }
	def put(self, request):
		data = request.data
		cart_item = CartItems.objects.get(id=data.get('id'))
		quantity = data.get('quantity')
		cart_item.quantity += quantity
		cart_item.save()
		return Response({'success': 'Item Updated Sccussfully'})





		

#TO DELETE ITEM IN A CART
#Eg:
#Pass id of the product
# {
#     "id":9
    
# }
	def delete(self, request):
		user = request.user
		data = request.data
		cart_item = CartItems.objects.get(id=data.get('id'))
		cart_item.delete()

		cart = Cart.objects.filter(user=user, ordered=False).first()
		queryset = CartItems.objects.filter(cart=cart)
		serializer = CartItemsSerializer(queryset, many=True)

		return Response(serializer.data)


