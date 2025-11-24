from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import SignupSerializer, LoginSerializer, CategorySerializer, AppointmentSerializer
from .models import Category, Appointment

# ------------------------------------------------
# New View for Listing Categories (GET)
# ------------------------------------------------
class CategoryListView(APIView):
    """
    Handles GET requests to return a list of all care categories (Prenatal, Postnatal, etc.).
    This endpoint is public.
    """
    def get(self, request):
        # 1. Fetch all category objects from the database
        # Ordering by name ensures the list is consistent
        categories = Category.objects.all().order_by('name')
        
        # 2. Serialize the queryset (use many=True for a list of objects)
        serializer = CategorySerializer(categories, many=True)
        
        # 3. Return the data in a successful response
        return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------------------------------
# Existing Authentication Views (Signup, Login)
# ------------------------------------------------

class SignupView(APIView):
    """
    Handles user registration (POST).
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Account created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login and token generation/return (POST).
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    # Safely retrieve the role attribute
                    "role": getattr(user, "role", None),
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Appointments View
class CreateAppointmentView(APIView):

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            appointment = serializer.save()

            # Send confirmation email
            subject = "Appointment Confirmation"
            message = (
                f"Hello {appointment.full_name},\n\n"
                f"Your appointment for {appointment.category.name} "
                f"has been scheduled.\n\n"
                f"📅 Date: {appointment.date}\n"
                f"⏰ Time: {appointment.time}\n"
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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
