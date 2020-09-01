from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomerRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = UserProfile
        fields = (
                  'user',
                  'address',
                  'mobile_number',
                  'is_branchOwner',
                ) 
    def create(self, validated_data):
        
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        customer, created = UserProfile.objects.update_or_create(user=user,
                            address=validated_data.pop('address'),mobile_number=validated_data.pop('mobile_number'),is_branchOwner = validated_data.pop('is_branchOwner'))
        return customer


class BranchOwnerRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = UserProfile
        fields = (
                  'user',
                  'address',
                  'mobile_number',
                  'is_branchOwner',
                  
                ) 
    def create(self, validated_data):
        
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        branchOwner, created = UserProfile.objects.update_or_create(user=user,
                            address=validated_data.pop('address'),mobile_number=validated_data.pop('mobile_number'),is_branchOwner = validated_data.pop('is_branchOwner'))
        return branchOwner