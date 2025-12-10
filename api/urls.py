from django.urls import path
from .views import LoginView, SignupView, CategoryListView, CreateAppointmentView

# SimpleJWT built-in views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Authentication
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),

    # JWT Helpers
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),

    # App Endpoints
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("appointments/create/", CreateAppointmentView.as_view(), name="create-appointment"),
]
