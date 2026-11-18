from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from trainer.models import Lesson

class LessonReview(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.PROTECT,
        related_name="review",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)