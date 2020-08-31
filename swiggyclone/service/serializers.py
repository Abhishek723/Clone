from rest_framework import serializers
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order
    )


class FoodItemSerializer(serializers.ModelSerializer):
    #branch_name = serializers.CharField(source = "branch.name",read_only=True)

    class Meta:
        model = FoodItem
        fields = (
                  'name',
                  'price',
                  'quantity',
                )



class OrderSerializers(serializers.ModelSerializer):
    foodItems = FoodItemSerializer(many=True)
    class Meta:
        model = Order
        feilds = (
                'order_time',
                'total_price',
                'quantity',
                'foodItems'
            )

     def create(self, validated_data):
        foodItems_data = validated_data.pop('foodItems')
        order = Order.objects.create(**validated_data)
        for foodItem_data in foodItems_data:
            FoodItem.objects.create(order=order, **foodItem_data)
        return order


class BranchSerializer(serializers.ModelSerializer):
    foodItems = FoodItemSerializer(many=True)
    orders = OrderSerializers(many=True)
    class Meta:
        model = Branch
        fields = (
                  'name',
                  'address',
                  'pincode',
                  'foodItems',
                  'orders'
                )
    def create(self, validated_data):
        foodItems_data = validated_data.pop('foodItems')
        order_data = validated_data.pop('orders')
        branch = Branch.objects.create(**validated_data)
        for foodItem_data in foodItems_data:
            FoodItem.objects.create(branch=branch, **foodItem_data, ** order_data)
        return branch
                
class RestaurentSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True)
    class Meta:
        model = Restaurent
        fields = ('name',
                  'discription',
                  'branches'
                )
    def create(self, validated_data):
        branches_data = validated_data.pop('branches')
        restaurent = Restaurent.objects.create(**validated_data)
        for branch_data in branches_data:
            Restaurent.objects.create(restaurent=restaurent, **branch_data)
        return restaurent


