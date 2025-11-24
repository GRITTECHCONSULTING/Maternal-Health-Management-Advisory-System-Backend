# api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Provider, Category

# ----------------------------
# Custom User Admin
# ----------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


# ----------------------------
# Patient Admin
# ----------------------------
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'address')
    search_fields = ('user__username', 'user__email')


# ----------------------------
# Provider Admin
# ----------------------------
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'license_number')
    search_fields = ('user__username', 'user__email', 'specialty')


# ----------------------------
# Category Admin
# ----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
