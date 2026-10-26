from django.db import models

class TrainerInfo(models.Model):
    GENDER = [
        ("male", "男性"),
        ("female", "女性"),
        ("other", "その他"),
        ("none", "回答しない"),
    ]
    
    name = models.TextField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(choices=GENDER, default="回答しない")
    speciality_genre = models.TextField()
    career = models.TextField()
    area = models.TextField()
    contacts = models.TextField()
    comment = models.TextField()
    feedback_fee = models.IntegerField()
    lesson_fee = models.IntegerField()