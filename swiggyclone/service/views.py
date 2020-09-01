from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
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
