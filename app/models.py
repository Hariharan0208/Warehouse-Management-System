from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class userdetails(AbstractUser):   
    Address=models.CharField(max_length=30)
    Phone=models.CharField(max_length=10)
    PanCard=models.CharField(max_length=10)
    UserType=models.CharField(max_length=10)
    Permission=models.CharField(max_length=10)
    Image=models.ImageField(upload_to="image/",null=True)
    is_user=models.BooleanField('Is user',default=False)
    is_agent=models.BooleanField('Is agent',default=False)


class Category(models.Model):
    categorys=models.CharField(max_length=300)

class ProductTable(models.Model):
    CategoryType=models.ForeignKey(Category,on_delete=models.CASCADE)
    ProductName=models.CharField(max_length=200)
    Description=models.TextField()
    Specifications=models.CharField(max_length=200,null=True)
    Price=models.IntegerField()
    Quantity=models.IntegerField()
    Image=models.ImageField(upload_to="image/")

class Cart(models.Model):
    user = models.ForeignKey(userdetails, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductTable, on_delete=models.CASCADE, null=True)
    Quantity = models.PositiveIntegerField(default=1,null=True)

    def total_price(self):
        if self.product:
            return self.Quantity * self.product.Price
        return 0

class ShipType(models.Model):
    type=models.CharField(max_length=300)

class Buy(models.Model):
    Customer=models.ForeignKey(userdetails, on_delete=models.CASCADE, null=True)
    OrderID=models.CharField(max_length=30,null=True)
    ProductName=models.CharField(max_length=30)
    Description=models.CharField(max_length=150)
    Specifications=models.CharField(max_length=150,null=True)
    Quentity=models.IntegerField()
    Price=models.IntegerField()
    TotalPrice=models.IntegerField()
    shiptype=models.ForeignKey(ShipType,on_delete=models.CASCADE)
    OrderDate=models.CharField(max_length=30)
    DeliverData=models.CharField(max_length=30)
    Agent=models.CharField(max_length=30,null=True,default='No')
    DeliveryStatus=models.CharField(max_length=30,null=True,default='Pending')
    Loaction=models.CharField(max_length=30,null=True,default='Location Not Update')
    PaymentMethod=models.CharField(max_length=30,null=True)
    DeliveryCondition=models.CharField(max_length=30,null=True)
    Image1 = models.ImageField(upload_to="image/", null=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('dispatched', 'Dispatched'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered'),
        ],null=True,default='Current Status Not Updated')

class Order(models.Model):
    DeliveryAgent=models.ForeignKey(userdetails,on_delete=models.CASCADE)
    OrderList=models.ForeignKey(Buy,on_delete=models.CASCADE)