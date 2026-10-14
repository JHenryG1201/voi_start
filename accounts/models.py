from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AccountType(models.TextChoices):
    STUDENT = 'student'
    TRAINER = 'trainer'

class Account(AbstractUser):
    account_type = models.CharField(
        choices=AccountType.choices,
        default=AccountType.STUDENT,
    )