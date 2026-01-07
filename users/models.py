from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, telegram_id, name = None, password = None, **extra_fields):
        if not telegram_id:
            raise ValueError("Telegram ID is required")

        user = self.model(
            telegram_id=telegram_id,
            name=name,
            **extra_fields
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, name="Admin", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        user = self.create_user(
            telegram_id=telegram_id,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
        TEACHER = "teacher", "Teacher"

    telegram_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"