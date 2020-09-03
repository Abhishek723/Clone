from accounts.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


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
    