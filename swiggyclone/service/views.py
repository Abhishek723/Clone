from django.db import transaction
from rest_framework import viewsets
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
    serializer_class = RestaurentSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().prefetch_related('foodItems')
    serializer_class = BranchSerializer
    def get_queryset(self):
        return Branch.objects.filter(restaurent_id = self.kwargs['restaurent_pk'])

    @action(detail=True, methods=['POST'])
    def placeOrder(self, request, pk, restaurent_pk):
        branch = self.get_object()
        foodItems = FoodItem.objects.filter(branch=branch)
        foodItemsSerializer = FoodItemSerializer(foodItems, many=True)
        data = request.data
        data["user"] = request.user
        orderSerializers = OrderSerializers(data=data)
        total_price = 0
        orderValid = True
        if orderSerializers.is_valid():
            orderDiscriptions = data['orderDiscriptions']
            orderedBranch = data['branch']
            for orderDiscription in orderDiscriptions:
                orderFoodItem = orderDiscription['foodItem']
                orderQuantity = orderDiscription['quantity']
                try: 
                    instance = FoodItem.objects.filter(branch_id=orderedBranch, id=orderFoodItem)
                except:
                    orderValid = False
                if orderValid:
                    serialize = FoodItemSerializer(instance.first())
                    foodItemQuantity = serialize.data["quantity"]
                    if foodItemQuantity - orderQuantity<0:
                        orderValid = False
                          
            if orderValid:
                for orderDiscription in orderDiscriptions:
                    orderFoodItem = orderDiscription['foodItem']
                    orderQuantity = orderDiscription['quantity']
                    instance = FoodItem.objects.filter(branch_id=orderedBranch, id=orderFoodItem)
                    foodItemPrice = instance.first().price
                    finalQuantity = instance.first().quantity - orderQuantity
                    update_serializer = FoodItemSerializer(instance.first(), data = {"quantity":finalQuantity}, partial = True)
                    if update_serializer.is_valid():
                        update_serializer.save()
                        total_price = total_price + orderQuantity*foodItemPrice
                        
                    else:
                        return Response(update_serializer.errors,status = 400)
                data["user"] = request.user
                orderSerializers.save()
        else:
            orderValid = False
            return Response(orderSerializers.errors,status = 404)
        if orderValid:
            return Response({"message":"Order Placed"}, status = 200)
        return Response({"message":"Food Item is not present"},status = 404)
        


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    def get_queryset(self):
        return FoodItem.objects.filter(branch_id = self.kwargs['branch_pk'])