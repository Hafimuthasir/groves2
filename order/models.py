from django.db import models

# Create your models here.

from django.db import models
from app_ga.models import myusers
from app_ga.models import products
from app_ga.models import Address
# from app_ga.models import Address
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(myusers,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out of delivery','Out of delivery'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    user = models.ForeignKey(myusers, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(myusers, on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,default='Confirmed')

    def _str_(self):
        return self.product.product_name

class wallet(models.Model):
    user = models.ForeignKey(myusers,on_delete=models.CASCADE)
    balance = models.IntegerField()

