from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from service.models import Branch
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500, blank=True)
    mobile_number = models.CharField(max_length = 10,blank = True) 
    is_branchOwner = models.BooleanField(default=False)
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE,blank=True,null= True)