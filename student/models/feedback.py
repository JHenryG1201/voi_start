from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os

from trainer.models import TrainerInfo

def audio_upload_path(instance, filename):
    return f"feedback_audio/{instance.student.id}/{filename}"

class Feedback(models.Model):
    STATUS = [
        ("pending", "未受取"),
        ("done", "受取済み"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="feedback_requests",
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="feedbacks",
    )

    audio = models.FileField(
        upload_to=audio_upload_path,
        validators=[FileExtensionValidator(["mp3", "wav", "m4a", "ogg", "webm"])],
    )

    price = models.IntegerField()
    content = models.TextField(null=True)
    feedback = models.TextField(null=True)
    status = models.CharField(max_length=7, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_time = models.DateTimeField(null=True)

    @property
    def audio_filename(self):
        return os.path.basename(self.audio.name)