from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.
class AccountType(models.TextChoices):
    STUDENT = 'student'
    TRAINER = 'trainer'

class Account(AbstractUser):
    username = models.CharField(
        error_messages={
            'unique': 'アカウントが既に作成されています。',
        },
        help_text='必要・150文字以下・文字/数字/@/./+/-/_だけ.',
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