from django.contrib import admin
from service.models import Restaurent, Branch, FoodItem, Order, OrderDiscription


admin.site.register(Branch)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderDiscription)
admin.site.register(Restaurent)
