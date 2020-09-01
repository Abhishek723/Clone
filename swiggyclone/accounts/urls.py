from accounts.views import UserRegistertionView,UpdateFoodItemView
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('BranchOwner/update/fooditems/<int:id>/edit',UpdateFoodItemView().as_view(),name = 'updateFoodItem'),
    path('register/',UserRegistertionView().as_view(),name = 'userRegistration'),
]
