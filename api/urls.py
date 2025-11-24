from django.urls import path, include
from .views import LoginView, SignupView, CategoryListView, CreateAppointmentView


urlpatterns = [
    # authentication endpoints
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    
    
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("appointments/create/", CreateAppointmentView.as_view(), name="create-appointment"),
]