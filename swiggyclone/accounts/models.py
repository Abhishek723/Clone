from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=True)
    mobile_number = models.CharField(max_length=10, blank=True)
    is_branchOwner = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
