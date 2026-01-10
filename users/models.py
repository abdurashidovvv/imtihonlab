from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, name, phone_number, password=None, role="user"):
        if not telegram_id:
            raise ValueError("Telegram ID is required")
        if not name:
            raise ValueError("Name is required")
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(
            telegram_id=telegram_id,
            name=name,
            phone_number=phone_number,
            role=role,
            is_staff=(role == "admin"),
            is_active=True,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, name, phone_number, password):
        user = self.create_user(
            telegram_id=telegram_id,
            name=name,
            phone_number=phone_number,
            password=password,
            role="admin"
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"

    telegram_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = ["name", "phone_number"]

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"
