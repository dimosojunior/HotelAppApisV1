from . import views
from django.urls import path


urlpatterns = [

    path('', views.HotelView, name='Hotel'),

    path('HotelFoodProducts/', views.HotelFoodProductsView, name='HotelFoodProducts'),
    path('HotelInentoryFood/', views.HotelInventoryFoodView, name='HotelInventoryFood'),

    path('Cart/', views.CartView.as_view(), name='Cart'),
    
]