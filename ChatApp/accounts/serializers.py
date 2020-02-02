from rest_framework import serializers
from .models import Account


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username', 'email', 'password']


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'password']


class UserForgotPassordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email']
