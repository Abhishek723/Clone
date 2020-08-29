from django.db import models
from django.utils import timezone


# Create your models here.
class Restaurent(models.Model):
    name = models.CharField(max_length = 200)
    discription = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length = 200) 
    address = models.TextField(max_length=500)
    restaurent = models.ForeignKey(Restaurent, on_delete=models.CASCADE)
    pincode = models.CharField(max_length = 6)
    # branchOwner = models.OneToOneField(BranchOwner, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length = 200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Order(models.Model):
    branch = models.IntegerField()
    foodItem = models.IntegerField()
    order_time = models.DateTimeField(default=timezone.now)
    total_price = models.IntegerField(default=0)
    quantity = models.IntegerField()
