from rest_framework import serializers
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order,
    OrderDiscription
    )


class OrderDiscriptionSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = OrderDiscription
        fields = (
                'id',
                'price',
                'quantity', 
                'foodItem'  
            )

    

class FoodItemSerializer(serializers.ModelSerializer):
    orderDiscriptions = OrderDiscriptionSerializers(many=True,required=False)
    class Meta:
        model = FoodItem
        fields = (
                  'id',
                  'name',
                  'price',
                  'quantity',
                  'orderDiscriptions',
                  
                )


class OrderSerializers(serializers.ModelSerializer):
    orderDiscriptions = OrderDiscriptionSerializers(many=True)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Order
        fields = (
                'id',
                'order_time',
                'total_price',
                'orderDiscriptions',
                'branch'
            )

    def create(self, validated_data):
        orderDiscriptions_data = validated_data.pop('orderDiscriptions')
        order = Order.objects.create(**validated_data)
        for orderDiscription_data in orderDiscriptions_data:
            foodItem = orderDiscription_data['foodItem']
            quantity = orderDiscription_data['quantity'] 
            OrderDiscription.objects.create(order=order, **orderDiscription_data)
        return order


class BranchSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Branch
        fields = (
                  'id',
                  'name',
                  'address',
                  'pincode',    
                  'branchOwner',
                  'restaurent'
                )
    


class RestaurentSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Restaurent
        fields = (
                  'id',
                  'name',
                  'discription',
                )
    



