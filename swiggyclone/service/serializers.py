from rest_framework import serializers
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order,
    OrderDiscription
    )


class OrderDiscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderDiscription
        feilds = (
                'id',
                'price',
                'quantity',   
            )



class FoodItemSerializer(serializers.ModelSerializer):
    orderDiscriptions = OrderDiscriptionSerializers(many=True, read_only=True)
    class Meta:
        model = FoodItem
        fields = (
                  'id',
                  'name',
                  'price',
                  'quantity',
                  'orderDiscriptions'
                )


class OrderSerializers(serializers.ModelSerializer):
    orderDiscriptions = OrderDiscriptionSerializers(many=True, read_only=True)
    class Meta:
        model = Order
        feilds = (
                'id',
                'order_time',
                'total_price',
                'orderDiscriptions'
            )

    def create(self, validated_data):
        orderDiscriptions_data = validated_data.pop('orderDiscriptions')
        order = Order.objects.create(**validated_data)
        for orderDiscription_data in orderDiscriptions_data:
            OrderDiscription.objects.create(order=order, **orderDiscription_data)
        return order


class BranchSerializer(serializers.ModelSerializer):
    foodItems = FoodItemSerializer(many=True)
    orders = OrderSerializers(many=True)
    class Meta:
        model = Branch
        fields = (
                  'id',
                  'name',
                  'address',
                  'pincode',
                  'foodItems',
                  'orders',
                )
    def create(self, validated_data):
        foodItems_data = validated_data.pop('foodItems')
        orders_data = validated_data.pop('orders')
        branch = Branch.objects.create(**validated_data)
        for foodItem_data in foodItems_data:
            FoodItem.objects.create(branch=branch, **foodItem_data)
        for order_data in orders_data:
            Order.objects.create(branch=branch, ** order_data)
        return branch


class RestaurentSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True)
    class Meta:
        model = Restaurent
        fields = (
                  'name',
                  'discription',
                  'branches',
                )
    def create(self, validated_data):
        branches_data = validated_data.pop('branches')
        restaurent = Restaurent.objects.create(**validated_data)
        for branch_data in branches_data:
            Branch.objects.create(restaurent=restaurent, **branch_data)
        return restaurent


