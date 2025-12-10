from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    CategorySerializer,
    AppointmentSerializer
)
from .models import Category, Appointment
from django.contrib.auth import authenticate


# ------------------------------------------------
# 1. List Categories (GET)
# ------------------------------------------------
class CategoryListView(generics.ListAPIView):
    """
    Returns a list of all care categories (Prenatal, Postnatal, etc.).
    Public endpoint.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("name")


# ------------------------------------------------
# 2. Signup View (POST) with JWT token return
# ------------------------------------------------
class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "message": "Account created successfully",
                "access": str(access),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": getattr(user, "role", None),
                },
            },
            status=status.HTTP_201_CREATED,
        )


# ------------------------------------------------
# 3. Login View (POST) with JWT token return
# ------------------------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "message": "Login successful",
                "access": str(access),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": getattr(user, "role", None),
                }
            },
            status=status.HTTP_200_OK
        )


# ------------------------------------------------
# 4. Create Appointment (POST)
# ------------------------------------------------
class CreateAppointmentView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def perform_create(self, serializer):
        appointment = serializer.save()

        # Send confirmation email
        subject = "Appointment Confirmation"
        message = (
            f"Hello {appointment.name},\n\n"
            f"Your appointment for {appointment.category.name} has been scheduled.\n\n"
            f"📅 Date: {appointment.time.date()}\n"
            f"⏰ Time: {appointment.time.time()}\n"
            f"📍 Category: {appointment.category.name}\n\n"
            f"Thank you!"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [appointment.email],
            fail_silently=False,
        )

        # Mark as confirmed
        appointment.is_confirmed = True
        appointment.save()
