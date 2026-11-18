from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from student.models import Feedback

class FeedbackReview(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.PROTECT,
        related_name="review",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)