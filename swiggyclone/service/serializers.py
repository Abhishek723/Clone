from rest_framework import serializers
from service.models import (
    Restaurent,
    Branch, 
    FoodItem, 
    Order, 
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

class BranchSerializer(serializers.ModelSerializer):
    foodItems = FoodItemSerializer(many=True)
    #restaurent = serializers.CharField(source = "restaurent.name",read_only= True)
    class Meta:
        model = Branch
        fields = (
                  'name',
                  'address',
                  'pincode',
                  'foodItems',
                )
    def create(self, validated_data):
        foodItems_data = validated_data.pop('foodItems')
        branch = Branch.objects.create(**validated_data)
        for foodItem_data in foodItems_data:
            FoodItem.objects.create(branch=branch, **foodItem_data)
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