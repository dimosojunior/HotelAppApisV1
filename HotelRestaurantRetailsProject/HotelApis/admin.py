from django.contrib import admin
from HotelApis.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'password1', 'password2'),
        }),
    )

    ordering=('email',)




class HotelInventoryAdmin(admin.ModelAdmin):

    list_display = ["Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]


class ProductAdmin(admin.ModelAdmin):

    list_display = ["id","product_name","price","ProductQuantity","ProductUnit","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["product_name"]

class CartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(HotelInventory, HotelInventoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)