from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import PrependedText
from django import forms

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=300)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=255)
    state = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    warehouse_number = models.IntegerField(blank=False) 


    # foreign key
    # authenticated/not authenticated users
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        
        return 'Адреса доставки №' + str(self.id)    
    
class Order(models.Model):
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)  

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    date_ordered = models.DateTimeField(auto_now_add=True)

    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Замовлення №' + str(self.id)
    
    
    
class OrderItem(models.Model): 
    # FK ->
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1) 
    price = models.DecimalField(max_digits=8, decimal_places=2) 
    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        
        return 'Товар №' + str(self.id)   
    
    def get_total(self):
        return self.quantity * self.price
    

