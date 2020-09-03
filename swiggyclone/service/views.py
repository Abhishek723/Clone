
from django.db import transaction
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order,
    OrderDiscription
    )
from service.serializers import (
    FoodItemSerializer,
    RestaurentSerializer, 
    BranchSerializer,
    OrderSerializers,
    OrderDiscriptionSerializers
    )


class RestaurentViewSet(viewsets.ModelViewSet):
    queryset = Restaurent.objects.all().prefetch_related('branches')
    serializer_class = RestaurentSerializers


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().prefetch_related('foodItems')
    serializer_class = BranchSerializer
    def get_queryset(self):
        return Branch.objects.select_related('foodItem').filter(restaurent_id = self.kwargs['restaurent_pk'])

    @action(detail=True, method=['POST'])
    def placeOrder(self, request, pk):
        branch = self.get_object()
        foodItems = FoodItem().objects.filter(branch=branch)
        foodItemsSerializer = FoodItemSerializer(foodItems, many=True)
        orderSerializers = OrderSerializers(data=request.data)
        if orderSerializers.is_valid():
            data = orderSerializers.data
            orderDiscriptions = data['orderDiscriptions']
            total_price = 0
            for orderDiscription in orderDiscriptions:
                orderFoodItem = orderDiscription['foodItem']
                orderQuantity = orderDiscription['quantity']
                instance = FoodItem.filter(branch_id=orderedBranch, id=orderFoodItem)
                foodItemPrice = instance.first().price
                finalQuantity = instance.first().quantity - orderQuantity
                serializer = FoodItemSerializer(instance.first(), data = {"quantity":finalQuantity}, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    total_price = total_price + orderQuantity*foodItemPrice
                else:
                    return Response(serializer.errors,status = 400)
        else:
            Response(serializer.errors,status = 404)
        
        return Response({"message":"Order Placed", "total Price":total_price}, status = 200)


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    def get_queryset(self):
        return FoodItem.objects.filter(restaurent_id = self.kwargs['restaurent_pk'], branch_id = self.kwargs['branch_pk'])