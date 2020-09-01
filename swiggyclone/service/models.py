from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


# Create your models here.
class Restaurent(models.Model):
    name = models.CharField(max_length = 200)
    discription = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length = 200) 
    address = models.TextField(max_length=500)
    restaurent = models.ForeignKey(Restaurent,related_name='branches', on_delete=models.CASCADE)
    branchOwner = models.ForeignKey(User,related_name='branches', on_delete=models.CASCADE)
    pincode = models.CharField(max_length = 6)
    def __str__(self):
        return self.name




class FoodItem(models.Model):
    name = models.CharField(max_length = 200)
    price = models.PositiveIntegerField()
    quantity = models.IntegerField()
    branch = models.ForeignKey(Branch,related_name='foodItems', on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class Order(models.Model):
    user = models.ForeignKey(User,related_name='orders', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,related_name='orders', on_delete=models.CASCADE)
    order_time = models.DateTimeField(default=timezone.now)
    total_price = models.PositiveIntegerField()


class OrderDiscription(models.Model):
    order = models.ForeignKey(Order,related_name='orderDiscriptions', on_delete=models.CASCADE)
    foodItem = models.ForeignKey(FoodItem,related_name='orderDiscriptions', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()