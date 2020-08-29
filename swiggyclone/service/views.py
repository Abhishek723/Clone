from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order
    )

from service.serializers import (
    FoodItemSerializer,
    RestaurentSerializer, 
    BranchSerializer
    )
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class PlaceOrder(APIView):

    def put(self, request, id, format=None):
        orderedBranch = data['branchId']
        #print(orderedBranch)
        for orderItem in data['orderList']:
            
            orderFoodItem = orderItem['orderFoodItemId']
            orderQuantity = orderItem['quantity']
            print("orderFoodItem",orderFoodItem)
            print("orderQuantity",orderQuantity)
            try:
                instance = FoodItem.objects.filter(branch_id=orderedBranch, id=orderFoodItem)
            except FoodItem.DoesNotExist as e:
                return Response({'error':'Given fooditem not found'},status = 404)
            print("instance[0].quantity",instance[0].quantity)
            if instance[0].quantity < orderQuantity:
                return Response({'error':'Given fooditem not found'},status = 404)
        total_price = 0
        for orderItem in data['orderList']:
            print("orderFoodItem",orderFoodItem)
            print("orderQuantity",orderQuantity)
            orderFoodItem = orderItem['orderFoodItemId']
            orderQuantity = orderItem['quantity']
            instance = FoodItem.objects.filter(branch_id=orderedBranch, id=orderFoodItem)
            foodItemPrice = instance[0].price
            finalQuantity = instance[0].quantity - orderQuantity
            serializer = FoodItemSerializer(instance[0],data = {"quantity":finalQuantity},partial = True)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                total_price = total_price + orderQuantity*foodItemPrice
            else:
                return Response(serializer.errors,status = 400)
        # updateData = FoodItem.objects.filter(branch_id=orderedBranch)
        # finalSerializer = FoodItemSerializer(updateData,many = True)
        # json = JSONRenderer().render(finalSerializer.data)
        return Response({"message":"Order Placed","total Price":total_price},status = 200)


class BranchRegistertionView(APIView):

    def post(self,request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

class RestaurentRegistertionView(APIView):

    def post(self,request):
        serializer = RestaurentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

class FoodItemRegistertionView(APIView):

    def post(self,request):
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)
