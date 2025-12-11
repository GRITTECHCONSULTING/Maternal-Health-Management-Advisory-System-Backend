from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    CategorySerializer,
    AppointmentSerializer,
    UserSerializer
)
from .models import Category, Appointment

# ------------------------------------------------
# Logout Serializer (Swagger/OpenAPI-friendly)
# ------------------------------------------------
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        required=True,
        help_text="Refresh token to blacklist for logout"
    )

    swagger_schema_fields = {
        "example": {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    }


# ------------------------------------------------
# 1. List Categories (GET)
# ------------------------------------------------
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("name")
    permission_classes = [AllowAny]


# ------------------------------------------------
# 2. Signup (POST) — Returns JWT Tokens
# ------------------------------------------------
class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Account created successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )


# ------------------------------------------------
# 3. Login (POST) — Returns JWT Tokens
# ------------------------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )


# ------------------------------------------------
# 4. Logout View
# ------------------------------------------------
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        """
        Logout by blacklisting the provided refresh token.

        Headers:
            Authorization: Bearer <access_token>

        Body:
            {
                "refresh": "<refresh_token>"
            }

        Responses:
            200: Logged out successfully
            400: Invalid or expired refresh token
            401: Access token missing or invalid
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

# ------------------------------------------------
# 5. Get Logged-in User Profile (GET)
# ------------------------------------------------
class UserProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "message": "User profile fetched successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )


# ------------------------------------------------
# 6. Create Appointment (POST)
# ------------------------------------------------
class CreateAppointmentView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        appointment = serializer.save()

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

        appointment.is_confirmed = True
        appointment.save()
