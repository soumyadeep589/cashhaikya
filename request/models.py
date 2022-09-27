from django.db import models
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _


class Request(models.Model):
    class Status(models.TextChoices):
        REQUEST = "RQ", _("Request")
        PARTIALLY_SETTLED = "PS", _("Partially Settled")
        CLOSED = "CL", _("Closed")
        DELETED = "DL", _("Deleted")

    class Type(models.TextChoices):
        CASH = "C", _("Cash")
        BANK = "B", _("Bank")

    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    type = models.CharField(max_length=16, choices=Type.choices, default=Type.BANK)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.REQUEST
    )
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "request"
        verbose_name_plural = "request"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}, name: {self.user.id}, amount: {self.amount}"
