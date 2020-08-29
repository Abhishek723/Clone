from django.contrib import admin
from django.urls import path,include
from accounts.views import UserRegistertionView
from accounts.views import UpdateFoodItemView
urlpatterns = [
    path('BranchOwner/update/fooditems/<int:id>/edit',UpdateFoodItemView().as_view(),name = 'updateFoodItem'),
    path('register/',UserRegistertionView().as_view(),name = 'userRegistration'),
]
