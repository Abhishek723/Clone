from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from service.models import Branch
from accounts.serializers import BranchOwnerRegisterSerializer,CustomerRegisterSerializer
from accounts.models import UserProfile
from service.models import FoodItem
from rest_framework.views import APIView
from service.serializers import FoodItemSerializer
# Create your views here.


class UserRegistertionView(APIView):

    def post(self,request):
        is_branchOwner = request.data['is_branchOwner']
        if is_branchOwner:
            serializer = BranchOwnerRegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=ValueError):
                serializer.create(validated_data=request.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=ValueError):
                serializer.create(validated_data=request.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)



class UpdateFoodItemView(APIView):

    def put(self, request, id):
        is_branchOwner = request.data['is_branchOwner']
        if is_branchOwner:
            try:
                instance = FoodItem.objects.get(id = id)
            except FoodItem.DoesNotExist as e:
                return Response({"error":"Given Food Item is not found"},status = 404)
            finalQuantity = request.data['quantity']
            serializer = FoodItemSerializer(instance,data = {"quantity":finalQuantity},partial = True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status = 200)
            else:
                return JsonResponse(serializer.errors,status = 400)
        else:
            return Response({"message": "Permission Denied"},status = 403)