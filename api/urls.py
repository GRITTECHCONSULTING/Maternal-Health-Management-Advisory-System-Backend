from django.urls import path, include
from .views import LoginView, SignupView, CategoryListView


urlpatterns = [
    # authentication endpoints
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    
    # endpoint for listing categories
    path("categories/", CategoryListView.as_view(), name="category-list"),
]