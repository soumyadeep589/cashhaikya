from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(unique=True)
    name = models.CharField(max_length=256)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiration_date = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    transactions = models.IntegerField(default=0)
    note = models.TextField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        ordering = ["id"]

    def __str__(self):
        return str(self.phone)

    def is_otp_expired(self):
        return self.otp_expiration_date < timezone.now()
