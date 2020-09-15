from rest_framework import serializers

from service.models import Restaurent, Branch, FoodItem, Order, OrderDiscription


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'quantity']

    def create(self, validated_data):
        try:
            int(self.context.get("branch"))
        except ValueError:
            raise serializers.ValidationError({"detail": "input is not valid"})

        validated_data['branch_id'] = self.context.get("branch",None)
        foodItem = FoodItem.objects.create(**validated_data)
        return foodItem

class OrderDiscriptionSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OrderDiscription
        fields = ['id', 'price', 'quantity', 'foodItem']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['foodItem'] = FoodItemSerializer(instance.foodItem).data
        return response


class OrderSerializers(serializers.ModelSerializer):
    orderDiscriptions = OrderDiscriptionSerializers(many=True)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Order
        fields = ['id', 'order_time', 'orderDiscriptions', 'branch', 'user']

    def validate(self, data):
        orderDiscriptions_data = data['orderDiscriptions']
        for orderDiscription_data in orderDiscriptions_data:
            orderFoodItem = orderDiscription_data['foodItem']
            orderQuantity = orderDiscription_data['quantity']
            foodItemQuantity = orderDiscription_data['foodItem'].quantity
            if foodItemQuantity < orderQuantity:
                raise serializers.ValidationError('Given fooditem not found.')
        return data

    def create(self, validated_data):
        orderDiscriptions_data = validated_data.pop('orderDiscriptions')
        total_price = 0
        for orderDiscription_data in orderDiscriptions_data:
            price = orderDiscription_data['price']
            foodItemQuantity = orderDiscription_data['foodItem'].quantity
            orderQuantity = orderDiscription_data['quantity']
            total_price += price * orderQuantity
        order = Order.objects.create(**validated_data, total_price=total_price)
        for orderDiscription_data in orderDiscriptions_data:
            updated_quantity = orderDiscription_data['foodItem'].quantity - int(orderDiscription_data['quantity'])
            data = {"quantity": updated_quantity}
            serializer = FoodItemSerializer(orderDiscription_data['foodItem'], data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                OrderDiscription.objects.create(order=order, **orderDiscription_data)
        return order


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'pincode']

    def create(self, validated_data):
        try:
            int(self.context.get('restaurent'))
        except ValueError:
            raise serializers.ValidationError({"detail": "input is not valid"})
        request = self.context.get('request', None)
        validated_data['restaurent_id'] = self.context.get("restaurent",None)
        validated_data['branchOwner'] = request.user
        branch = Branch.objects.create(**validated_data)
        return branch



class RestaurentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurent
        fields = ['id', 'name', 'discription']
