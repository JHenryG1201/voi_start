from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.
class AccountType(models.TextChoices):
    STUDENT = 'student'
    TRAINER = 'trainer'

class Account(AbstractUser):
    # ドメインモデルではメールアドレス
    username = models.CharField(
        error_messages={
            'unique': 'A user with that username already exists.',
        },
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=150,
        unique=False,
        validators=[UnicodeUsernameValidator()],
        verbose_name='username',
    )
    account_type = models.CharField(
        choices=AccountType.choices,
        default=AccountType.STUDENT,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'account_type'],
                name='unique_username_per_account_type',
            ),
        ]