from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "name", "phone_number", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("telegram_id", "name", "phone_number")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("telegram_id", "name", "phone_number", "password")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("telegram_id", "name", "phone_number", "password1", "password2", "role", "is_staff",
                       "is_active"),
        }),
    )
