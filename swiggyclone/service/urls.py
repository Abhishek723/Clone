from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from service.views import RestaurentViewSet, BranchViewSet, FoodItemViewSet


router = SimpleRouter()
router.register('restaurent', RestaurentViewSet)

restaurents_router = routers.NestedSimpleRouter(router, r'restaurent', lookup='restaurent')
restaurents_router.register(r'branches', BranchViewSet, basename='Branch')

branches_router = routers.NestedSimpleRouter(restaurents_router, r'branches', lookup='branch')
branches_router.register(r'foodItems', FoodItemViewSet, basename='FoodItem')

urlpatterns = [
    path('/', include(router.urls)),
    path('/', include(restaurents_router.urls)),
    path('/', include(branches_router.urls)),
]
