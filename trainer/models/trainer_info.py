from django.db import models
from django.conf import settings

class TrainerInfo(models.Model):
    GENDER = [
        ("male", "男性"),
        ("female", "女性"),
        ("other", "その他"),
        ("none", "回答しない"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trainer_profile",
    )
    
    name = models.TextField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=6, choices=GENDER, default="none")
    speciality_genre = models.TextField()
    career = models.TextField()
    area = models.TextField()
    contacts = models.TextField()
    comment = models.TextField()
    feedback_fee = models.IntegerField()
    lesson_fee = models.IntegerField()