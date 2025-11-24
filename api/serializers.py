# api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
# Import the new Category model from your models file
from .models import Category 

User = get_user_model()

# ------------------------------------------------
# 1. New Serializer for the Category Model
# ------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for listing and retrieving care categories.
    """
    class Meta:
        model = Category
        # Include all fields that you want to display for the categories
        fields = ('id', 'name', 'description', 'slug') 

# ------------------------------------------------
# 2. Existing User Serializers (Unchanged)
# ------------------------------------------------

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "role",
            "username",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Check if user exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Use username internally for Django authentication
        user = authenticate(username=user_obj.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data["user"] = user
        return data