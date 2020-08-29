from django.contrib import admin
from django.urls import path,include
from service.views import (
    PlaceOrder,
    RestaurentRegistertionView,
    BranchRegistertionView,
    FoodItemRegistertionView
)
urlpatterns = [
    path('',PlaceOrder.as_view(),name = 'placeOrder'),
    path('/register/restaurent/',RestaurentRegistertionView.as_view(),name = 'restaurentRegistertionView'),
    path('/register/branch/',BranchRegistertionView.as_view(),name = 'branchRegistertionView'),
    path('/register/fooditem/',FoodItemRegistertionView.as_view(),name = 'foodItemRegistertionView')
]
