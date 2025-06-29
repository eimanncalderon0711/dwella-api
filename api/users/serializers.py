from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'middlename', 'address', 'contact_number', 'role', 'profile', 'date_joined'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    profile = serializers.ImageField(required=False)

    class Meta: 
        model = CustomUser
        fields= [
            'first_name', 'last_name', 'middlename', 'username',
            'email', 'address', 'contact_number', 'role', 'password', 'profile', 'date_joined'
        ]

    def create (self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return user
        raise serializers.ValidationError("Invalid username or password")