from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
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


class PlaceOrder(APIView):
    @transaction.atomic
    def put(self, request, id, format=None):

        serialized_data = OrderSerializers(data=request.data)
        if serialized_data.is_valid():
            data = serialized_data.data
            orderedBranch = data['branchId']
            for orderItem in data['orderList']:
                
                orderFoodItem = orderItem['orderFoodItemId']
                orderQuantity = orderItem['quantity']
                try:
                    instance = FoodItem.objects.select_related('branch').filter(branch_id=orderedBranch, id=orderFoodItem)
                except FoodItem.DoesNotExist as e:
                    return Response({'error':'Given fooditem not found'},status = 404)
                
                if instance[0].quantity < orderQuantity:
                    return Response({'error':'Given fooditem not found'},status = 404)
            total_price = 0
            for orderItem in data['orderList']:
                orderFoodItem = orderItem['orderFoodItemId']
                orderQuantity = orderItem['quantity']
                instance = FoodItem.objects.select_related('branch').filter(branch_id=orderedBranch, id=orderFoodItem)
                foodItemPrice = instance.first().price
                finalQuantity = instance.first().quantity - orderQuantity
                serializer = FoodItemSerializer(instance[0], data = {"quantity":finalQuantity}, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    total_price = total_price + orderQuantity*foodItemPrice
                else:
                    return Response(serializer.errors,status = 400)
            serialized_data.save()
            return Response({"message":"Order Placed", "total Price":total_price}, status = 200)
        else:
            return Response({"error: request is not in valid format"},status=400)

class BranchRegistertionView(APIView):

    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

class RestaurentRegistertionView(APIView):

    def post(self, request):
        serializer = RestaurentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

class FoodItemRegistertionView(APIView):

    def post(self,request):
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


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
        data = orderSerializers.data
        orderDiscriptions = data['orderDiscriptions']
        branch = Branch.objects.select_related('foodItem').get(id=pk)
        for orderDiscription in orderDiscriptions:
            orderFoodItem = orderDiscription['foodItem']
            orderQuantity = orderDiscription['quantity']
            try:
                instance = FoodItem.filter(branch_id=orderedBranch, id=orderFoodItem)
            except FoodItem.DoesNotExist as e:
                return Response({'error':'Given fooditem not found'},status = 404)
            if instance[0].quantity < orderQuantity:
                return Response({'error':'Given fooditem not found'},status = 404)
        total_price = 0
        for orderDiscription in orderDiscriptions:
            orderFoodItem = orderDiscription['foodItem']
            orderQuantity = orderDiscription['quantity']
            instance = FoodItem.filter(branch_id=orderedBranch, id=orderFoodItem)
            foodItemPrice = instance.first().price
            finalQuantity = instance.first().quantity - orderQuantity
            serializer = FoodItemSerializer(instance[0], data = {"quantity":finalQuantity}, partial = True)
            if serializer.is_valid():
                serializer.save()
                total_price = total_price + orderQuantity*foodItemPrice
            else:
                return Response(serializer.errors,status = 400)
        
        return Response({"message":"Order Placed", "total Price":total_price}, status = 200)



class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    def get_queryset(self):
        return FoodItem.objects.filter(restaurent_id = self.kwargs['restaurent_pk'], branch_id = self.kwargs[branch_pk])