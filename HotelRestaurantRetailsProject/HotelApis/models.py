from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

    

  
class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    company_name=models.CharField(verbose_name="company name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone", max_length=15)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # Role_Choices = (
    #         ('MULTI TEACHER', 'MULTI TEACHER'),
    #         ('PHYSICS TEACHER', 'PHYSICS TEACHER'),
    #         ('CHEMISTRY TEACHER', 'CHEMISTRY TEACHER'),
    #         ('BIOLOGY TEACHER', 'BIOLOGY TEACHER'),
    #         ('ENGLISH TEACHER', 'ENGLISH TEACHER'),
    #         ('CIVICS TEACHER', 'CIVICS TEACHER'),
    #         ('MATHEMATICS TEACHER', 'MATHEMATICS TEACHER'),
    #         ('HISTORY TEACHER', 'HISTORY TEACHER'),
    #         ('GEOGRAPHY TEACHER', 'GEOGRAPHY TEACHER'),
    #         ('KISWAHILI TEACHER', 'KISWAHILI TEACHER'),
    #     )

    # role=models.CharField(verbose_name="role", choices=Role_Choices, max_length=50)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class HotelInventory(models.Model):

    Category = models.CharField(verbose_name="Category", max_length=100,blank=False,null=False)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/HotelInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Inventory"

    def __str__(self):
        return self.Category


class Product(models.Model):
    product_name = models.CharField(default="Wali", verbose_name="Product Name", max_length=100,blank=False,null=False)
    product_second_name = models.CharField(default="Maharage",verbose_name="Product Second Name", max_length=100,blank=True,null=True)
    price = models.CharField(max_length=20,blank=True,null=True)
    ProductUnit = models.CharField(verbose_name="Product Unit", max_length=100,blank=True,null=True)
    ProductQuantity = models.IntegerField(verbose_name="Product Quantity",blank=True,null=True)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/HotelInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        verbose_name_plural = "Product"
        
    
    def __str__(self):
        return self.product_name + " " + self.product_second_name





class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cart"

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cart Items"
    
    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name) + " " + str(self.product.product_second_name)
        
    

@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    # total_cart_items = CartItems.objects.filter(user = cart_items.user )
    # cart = Cart.objects.get(id = cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()