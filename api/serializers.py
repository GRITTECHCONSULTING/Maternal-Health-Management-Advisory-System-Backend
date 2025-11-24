from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Category, Appointment

User = get_user_model()


# ------------------------------------------------
# 1. Category Serializer
# ------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'slug')
        extra_kwargs = {
            'name': {'help_text': 'Name of the category'},
            'description': {'help_text': 'Description of the category'},
            'slug': {'help_text': 'URL-friendly slug'},
        }

    swagger_schema_fields = {
        "example": {
            "id": 1,
            "name": "Prenatal Care",
            "description": "Care for pregnant women",
            "slug": "prenatal-care"
        }
    }


# ------------------------------------------------
# 2. Signup Serializer
# ------------------------------------------------
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, help_text="User password")
    confirm_password = serializers.CharField(write_only=True, help_text="Confirm password")

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
        extra_kwargs = {
            'role': {'help_text': 'User role'},
            'username': {'help_text': 'Username'},
            'email': {'help_text': 'Email address'},
            'phone_number': {'help_text': 'Phone number'},
        }

    swagger_schema_fields = {
        "example": {
            "role": "patient",
            "username": "johndoe",
            "email": "john@example.com",
            "phone_number": "08012345678",
            "password": "StrongPass123!",
            "confirm_password": "StrongPass123!"
        }
    }

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


# ------------------------------------------------
# 3. Login Serializer
# ------------------------------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User email")
    password = serializers.CharField(write_only=True, help_text="User password")

    swagger_schema_fields = {
        "example": {
            "email": "john@example.com",
            "password": "StrongPass123!"
        }
    }

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        data["user"] = user
        return data


# ------------------------------------------------
# 4. Appointment Serializer
# ------------------------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    swagger_schema_fields = {
        "example": {
            "name": "John Doe",
            "email": "john@example.com",
            "time": "2025-11-25T14:00:00Z",
            "note": "First appointment",
            "category": 1
        }
    }

    def validate_time(self, value):
        if value.hour < 9 or value.hour >= 17:
            raise serializers.ValidationError("Time must be between 9 AM and 5 PM.")
        return value

    def validate_email(self, value):
        if not value or "@" not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value
