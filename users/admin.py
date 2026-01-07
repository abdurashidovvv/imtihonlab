from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "name", "role", "is_active")
    search_fields = ("telegram_id", "name")
