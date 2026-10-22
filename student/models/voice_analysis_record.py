from django.db import models
from django.conf import settings

class VoiceAnalysisRecord(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("complete", "Complete"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="voice_analysis_records",
    )

    audio = models.FileField(upload_to="voice-recordings/%Y/%m/%d/")
    song_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    low_note = models.CharField(max_length=32, blank=True)
    high_note = models.CharField(max_length=32, blank=True)
    tone_quality = models.TextField(blank=True)
    recommended_songs = models.JSONField(default=list)
    recommended_trainings = models.JSONField(default=list)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} - {self.created_at:%Y-%m-%d %H:%M}"