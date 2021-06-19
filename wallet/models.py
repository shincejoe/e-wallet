"""
AUTHOR: SHINCE JOE SHAJI
DATE: 20-06-21
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    customer_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4())


class Account(models.Model):
    status_choices = (
        (1, 'enabled'),
        (2, 'success'),
        (3, 'disabled')
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    status = models.IntegerField(choices=status_choices, null=True, blank=True, default=3)
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Account'
        app_label = 'wallet'
