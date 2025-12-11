from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    UserProfileView,
    CategoryListView,
    CreateAppointmentView,
)

urlpatterns = [
    # -------------------------
    # AUTHENTICATION ENDPOINTS
    # -------------------------
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", UserProfileView.as_view(), name="user-profile"),

    # -------------------------
    # CATEGORIES (PUBLIC DATA)
    # -------------------------
    path("categories/", CategoryListView.as_view(), name="category-list"),

    # -------------------------
    # APPOINTMENTS
    # -------------------------
    path("appointments/create/", CreateAppointmentView.as_view(), name="create-appointment"),
]
