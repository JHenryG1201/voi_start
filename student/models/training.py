from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class Training(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_trainings",
    )
    
    title = models.TextField(max_length=50)
    purpose = models.TextField()
    warning = models.TextField()
    duration = models.IntegerField()
    instructions = ArrayField(models.TextField())