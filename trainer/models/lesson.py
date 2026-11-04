from django.db import models
from django.conf import settings
from django.utils import timezone

class Lesson(models.Model):
    LESSON_TYPE = [
        ("online", "オンライン"),
        ("offline", "対面"),
        ("both", "どちらも対応可能"),
    ]

    LESSON_STATUS = [
        ("available", "予約可"),
        ("reserved", "予約中"),
        ("done", "実施済み"),
    ]

    lesson_date = models.DateField(null=True)
    lesson_start_time = models.TimeField(null=True)
    lesson_end_time = models.TimeField(null=True)
    lesson_place = models.TextField(null=True)
    lesson_type = models.CharField(max_length=7, choices=LESSON_TYPE, default="both")
    lesson_status = models.CharField(max_length=9, choices=LESSON_STATUS, default="available")

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="trainer_lessons",
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="student_lessons",
        null=True,
    )