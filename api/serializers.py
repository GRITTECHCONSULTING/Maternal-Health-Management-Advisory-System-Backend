# api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Category, Appointment

User = get_user_model()


# ------------------------------------------------
# 1. Serializer for Category Model
# ------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for listing and retrieving care categories.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'slug')


# ------------------------------------------------
# 2. User Serializers
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
# 3. Appointment Serializer
# ------------------------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate_time(self, value):
        """
        Ensure appointment time is between 9 AM and 5 PM.
        """
        if value.hour < 9 or value.hour >= 17:
            raise serializers.ValidationError("Time must be between 9 AM and 5 PM.")
        return value

    def validate_email(self, value):
        """
        Validate email format.
        """
        if not value or "@" not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value
