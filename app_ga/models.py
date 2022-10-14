from unicodedata import category
from django.db import models

# Create your models here.

class myusers(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.BigIntegerField()
    status = models.BooleanField(max_length=20,null=True)
    refferal_code = models.CharField(max_length = 50)
    applied_coupons = models.CharField(max_length=20,null=True)
    # blockstatus = models.CharField(max_length=10)
    
class admins(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class categories(models.Model):
    categoryname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/catgoryicons', height_field=None, width_field=None,null=True)

    def __str__(self):
        return self.categoryname

# class brands(models.Model):
#     product_brand = models.CharField(max_length=100)

class prodbrands(models.Model):
      productbrand = models.CharField(max_length=100,default=True)   

      def __str__(self):
          return self.productbrand
    
class carbrands(models.Model):
      carbrand = models.CharField(max_length=100,default=True)   
      carlogo = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,default=True)

      def __str__(self):
          return self.carbrand



class products(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    productname = models.CharField(max_length=100)
    price = models.BigIntegerField()
    dis_price=models.BigIntegerField(null=True)
    dis_price_type=models.CharField(max_length=100,null=True)
    dis_proprice=models.BigIntegerField(null=True)
    total_disprice=models.BigIntegerField(null=True)
    dis_perc = models.BigIntegerField(null=True)
    dis_applied = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    stocks =  models.CharField(max_length=100,default='1')
    stock_status = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    catid = models.ForeignKey(categories, on_delete=models.CASCADE)
    retrn = models.BooleanField(default=True)
    retrn_policy = models.CharField(max_length=10,null=True)
    carbrand = models.CharField(max_length=100)
    carbrid = models.ForeignKey(carbrands, on_delete=models.CASCADE,null=True)

    
    prodbrand = models.CharField(max_length=100)
    prodid = models.ForeignKey(prodbrands, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,default=True)
    image2 = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,)
    image3 = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,)
    image4 = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,)
    

class cart(models.Model):
    userid = models.ForeignKey(myusers, on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(products, on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length=100)
    total_price = models.CharField(max_length=100)




class guest_cart2(models.Model):
    user_session=models.CharField(max_length=20)
    productid = models.ForeignKey(products,on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length = 100)
    total_price = models.CharField(max_length = 100, null=True)

class wishlist(models.Model):
    userid = models.ForeignKey(myusers, on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(products, on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length=100)

class Address(models.Model):
      user_id=models.IntegerField()
      buyer_name=models.CharField(max_length=50)
      buyer_phone=models.CharField(max_length=11)
      address=models.CharField(max_length=100)
      pincode=models.CharField(max_length=7)
      city=models.CharField(max_length=50)
      state=models.CharField(max_length=30)
      country=models.CharField(max_length=50)

    
class guest_cart2(models.Model):
    user_session=models.CharField(max_length=20)
    productid = models.ForeignKey(products,on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length = 100)
    total_price = models.CharField(max_length = 100, null=True)

class Coupon(models.Model):
    coupon_number = models.CharField(max_length=16)
    start_date = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(null = True)
    discount_percentage = models.IntegerField(null = True)
    expiry_date = models.DateTimeField(auto_now=False)
    minimum_amount = models.IntegerField(default = 500)

class Coupon(models.Model):
    coupon_number = models.CharField(max_length=16)
    start_date = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(null = True)
    discount_percentage = models.IntegerField(null = True)
    expiry_date = models.DateTimeField(auto_now=False)
    minimum_amount = models.IntegerField(default = 500)

class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

class banner(models.Model):
    image = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,default=True)
    image2= models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,default=True)
    image3 = models.ImageField(upload_to='static/uploadedproducts', height_field=None, width_field=None,default=True)

class recent_products(models.Model):
    user = models.ForeignKey(myusers, on_delete=models.CASCADE,null=True)
    products = models.ForeignKey(products, on_delete=models.CASCADE,null=True)


class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()
