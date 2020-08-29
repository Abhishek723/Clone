from django.contrib import admin
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order, 
    )

# Register your models here.

admin.site.register(Restaurent)
admin.site.register(Branch)
admin.site.register(FoodItem)
admin.site.register(Order)

